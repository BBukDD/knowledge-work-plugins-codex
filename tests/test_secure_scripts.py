from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import sys
import zipfile
from argparse import Namespace
from pathlib import Path
from types import ModuleType

import pytest

from tools.build import BuildError, build_packages
from tools.validate import validate_package

PROJECT = Path(__file__).resolve().parents[1]
BIO_SCRIPTS = PROJECT / "plugins" / "kw-bio-research" / "skills" / "nextflow-development" / "scripts"
DATA_SCRIPT = (
    PROJECT / "plugins" / "kw-data" / "skills" / "data-context-extractor" / "scripts"
    / "package_data_skill.py"
)


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    prior_bytecode_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior_bytecode_setting
    return module


class FakeResponse(io.BytesIO):
    def __init__(self, data: bytes, url: str, content_length: str | None = None) -> None:
        super().__init__(data)
        self.url = url
        self.headers = {} if content_length is None else {"Content-Length": content_length}

    def geturl(self) -> str:
        return self.url


class FakeOpener:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = responses
        self.calls = 0

    def open(self, request: object, timeout: int) -> FakeResponse:
        self.calls += 1
        return self.responses.pop(0)


@pytest.fixture
def ncbi() -> ModuleType:
    return load_module(BIO_SCRIPTS / "utils" / "ncbi_utils.py", "secure_test_ncbi")


def test_ena_urls_are_https_and_restricted_to_expected_host(
    ncbi: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given typical ENA FTP values and a hostile host in a report.
    entries = (
        "run_accession\tsample_alias\tfastq_ftp\n"
        "SRR1\tsample\tftp.sra.ebi.ac.uk/vol1/fastq/SRR1_1.fastq.gz;"
        "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR1_2.fastq.gz\n"
        "SRR2\tsample\tevil.example/vol1/fastq/stolen.fastq.gz\n"
    )
    monkeypatch.setattr(ncbi, "HAS_REQUESTS", False)
    monkeypatch.setattr(ncbi, "urlopen", lambda *_args, **_kwargs: FakeResponse(entries.encode(), "https://www.ebi.ac.uk"))

    # When the ENA report is parsed.
    result = ncbi.fetch_ena_fastq_urls("SRP1")

    # Then only canonical HTTPS URLs on the expected host are returned.
    assert result == {
        "SRR1": [
            "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR1_1.fastq.gz",
            "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR1_2.fastq.gz",
        ]
    }


def test_download_uses_verified_cache_and_redownloads_tampering(
    ncbi: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given two complete offline responses for the same HTTPS FASTQ URL.
    url = "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR1.fastq.gz"
    opener = FakeOpener([FakeResponse(b"fresh", url, "5"), FakeResponse(b"fixed", url, "5")])
    monkeypatch.setattr(ncbi, "build_opener", lambda *_args: opener)
    target = tmp_path / "SRR1.fastq.gz"

    # When a download is reused and then its bytes are tampered with.
    assert ncbi.download_file(url, target, show_progress=False)
    assert ncbi.download_file(url, target, show_progress=False)
    target.write_bytes(b"wrong")
    assert ncbi.download_file(url, target, show_progress=False)

    # Then reuse required a matching URL, byte count, and SHA256 sidecar.
    assert opener.calls == 2
    assert target.read_bytes() == b"fixed"
    marker = json.loads((tmp_path / "SRR1.fastq.gz.download.json").read_text())
    assert marker == {"url": url, "size": 5, "sha256": hashlib.sha256(b"fixed").hexdigest()}


def test_truncated_download_keeps_existing_file_and_cleans_staging(
    ncbi: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given an unverified old file and a response shorter than Content-Length.
    url = "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR1.fastq.gz"
    target = tmp_path / "SRR1.fastq.gz"
    target.write_bytes(b"old")
    monkeypatch.setattr(ncbi, "build_opener", lambda *_args: FakeOpener([FakeResponse(b"short", url, "10")]))

    # When the replacement download is truncated.
    result = ncbi.download_file(url, target, show_progress=False)

    # Then the old file is left untouched but is not marked complete.
    assert not result
    assert target.read_bytes() == b"old"
    assert not (tmp_path / "SRR1.fastq.gz.download.json").exists()
    assert sorted(path.name for path in tmp_path.iterdir()) == ["SRR1.fastq.gz"]


@pytest.mark.parametrize(
    "redirect",
    ["http://ftp.sra.ebi.ac.uk/vol1/fastq/x.fastq.gz", "https://evil.example/x.fastq.gz"],
)
def test_download_redirect_rejects_insecure_target(ncbi: ModuleType, redirect: str) -> None:
    # Given an HTTPS ENA request redirected to an unsafe destination.
    from urllib.request import Request

    handler = ncbi.ENAHTTPSRedirectHandler()
    request = Request("https://ftp.sra.ebi.ac.uk/vol1/fastq/x.fastq.gz")

    # When urllib prepares to follow that redirect, it must reject the target.
    with pytest.raises(ValueError, match="ENA"):
        handler.redirect_request(request, None, 302, "Found", {}, redirect)


def test_packager_rejects_symlinks_and_output_inside_skill(tmp_path: Path) -> None:
    # Given a valid skill, an external secret, and an internal output directory.
    module = load_module(DATA_SCRIPT, "secure_test_packager")
    skill = tmp_path / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n")
    secret = tmp_path / "secret.txt"
    secret.write_text("secret")
    (skill / "leak.txt").symlink_to(secret)

    # When packaging a tree with a link or writing the ZIP into that tree.
    assert module.package_skill(str(skill), str(tmp_path / "outside")) is None
    (skill / "leak.txt").unlink()
    assert module.package_skill(str(skill), str(skill)) is None

    # Then no ZIP or external content was written.
    assert not list(tmp_path.rglob("*.zip"))


def test_packager_writes_only_regular_skill_files(tmp_path: Path) -> None:
    # Given a valid skill with a nested regular file.
    module = load_module(DATA_SCRIPT, "secure_test_packager_valid")
    skill = tmp_path / "skill"
    (skill / "data").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\n")
    (skill / "data" / "input.csv").write_text("a,b\n1,2\n")

    # When the skill is packaged outside its source tree.
    output = module.package_skill(str(skill), str(tmp_path / "outside"))

    # Then both expected files are present and the archive is readable.
    assert output is not None
    with zipfile.ZipFile(output) as archive:
        assert set(archive.namelist()) == {"skill/SKILL.md", "skill/data/input.csv"}


@pytest.mark.parametrize("parallel", [1, 2])
def test_download_command_verifies_existing_file_in_both_branches(
    tmp_path: Path, parallel: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given a partial existing FASTQ and an offline ENA run result.
    mock_ncbi = load_module(BIO_SCRIPTS / "utils" / "ncbi_utils.py", f"secure_test_ncbi_sra_{parallel}")
    mock_utils_package = ModuleType("utils")
    mock_utils_package.__path__ = []
    monkeypatch.setitem(sys.modules, "utils", mock_utils_package)
    monkeypatch.setitem(sys.modules, "utils.ncbi_utils", mock_ncbi)
    monkeypatch.setattr(sys, "path", list(sys.path))
    module = load_module(BIO_SCRIPTS / "sra_geo_fetch.py", f"secure_test_sra_{parallel}")
    url = "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR1.fastq.gz"
    target = tmp_path / "SRR1.fastq.gz"
    target.write_bytes(b"partial")
    monkeypatch.setattr(module, "fetch_sra_run_info_detailed", lambda _geo_id: [{"srr": "SRR1", "sra_study": "SRP1"}])
    monkeypatch.setattr(module, "group_samples_by_type", lambda _runs: {})
    monkeypatch.setattr(module, "fetch_ena_fastq_urls", lambda _study: {"SRR1": [url]})
    calls: list[Path] = []

    def fake_download(_url: str, path: Path, timeout: int, show_progress: bool) -> bool:
        calls.append(path)
        path.write_bytes(b"complete")
        return True

    monkeypatch.setattr(module, "download_file", fake_download)
    args = Namespace(
        geo_id="GSE1", output=str(tmp_path), subset=None, interactive=False,
        parallel=parallel, timeout=42,
    )

    # When the command runs with sequential or parallel execution.
    result = module.cmd_download(args)

    # Then the existing file goes through the same verification function.
    assert result == 0
    assert calls == [target]
    assert target.read_bytes() == b"complete"


@pytest.mark.parametrize(
    "tampered",
    ["skills/plain/SOURCE.md", "scripts/prepare.py"],
)
def test_package_inventory_detects_source_or_script_tampering(
    tmp_path: Path, tampered: str
) -> None:
    # Given a generated package with a SHA256 inventory in NOTICE.md.
    source = tmp_path / "source"
    module = source / "productivity"
    (module / ".claude-plugin").mkdir(parents=True)
    (module / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "productivity", "description": "Fixture", "author": {"name": "Anthropic"}})
    )
    (module / "LICENSE").write_text("Apache fixture")
    (module / "skills" / "plain").mkdir(parents=True)
    (module / "skills" / "plain" / "SKILL.md").write_text(
        "---\nname: plain\ndescription: Fixture\n---\n\nOriginal source.\n"
    )
    (module / "scripts").mkdir()
    (module / "scripts" / "prepare.py").write_text("print('fixture')\n")
    output = tmp_path / "output"
    build_packages(source, output, ("productivity",))
    package = output / "kw-productivity"
    assert validate_package(package) == []

    # When one preserved or runnable file changes after packaging.
    (package / tampered).write_text("tampered\n")

    # Then the inventory reports the exact changed path.
    assert any(tampered in error and "SHA256 inventory mismatch" in error for error in validate_package(package))


def test_builder_refuses_changed_upstream_script_preimage(tmp_path: Path) -> None:
    # Given an otherwise valid source module with one changed helper script.
    relative = Path("skills/nextflow-development/scripts/utils/ncbi_utils.py")
    source = tmp_path / "source"
    module = source / "bio-research"
    (module / ".claude-plugin").mkdir(parents=True)
    (module / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "bio-research", "description": "Fixture", "author": {"name": "Anthropic"}})
    )
    (module / "LICENSE").write_text("Apache fixture")
    (module / "skills" / "nextflow-development").mkdir(parents=True)
    (module / "skills" / "nextflow-development" / "SKILL.md").write_text(
        "---\nname: nextflow-development\ndescription: Fixture\n---\n\nOriginal source.\n"
    )
    (module / relative).parent.mkdir(parents=True)
    (module / relative).write_text("changed upstream")

    # When the builder stages that package.
    with pytest.raises(BuildError, match="preimage"):
        build_packages(source, tmp_path / "output", ("bio-research",))

