from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools import build as builder
from tools import validate as validator


def commit_source(source: Path) -> str:
    subprocess.run(["git", "init", "-q", str(source)], check=True)
    subprocess.run(["git", "-C", str(source), "add", "."], check=True)
    subprocess.run(
        [
            "git", "-C", str(source),
            "-c", "user.name=Codex Test",
            "-c", "user.email=codex-test@example.invalid",
            "-c", "commit.gpgsign=false",
            "commit", "-qm", "fixture",
        ],
        check=True,
    )
    return subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()


def make_productivity_source(source: Path) -> None:
    module = source / "productivity"
    (module / ".claude-plugin").mkdir(parents=True)
    (module / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "productivity",
                "description": "Upstream productivity workflows",
                "author": {"name": "Anthropic"},
            }
        ),
        encoding="utf-8",
    )
    (module / "LICENSE").write_text("Apache License fixture\n", encoding="utf-8")
    skill = module / "skills" / "sample"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: sample\ndescription: Use the sample workflow.\n---\n\nOriginal instructions.\n",
        encoding="utf-8",
    )


def test_verify_source_revision_rejects_ignored_skill_injection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given a committed source whose ignore rule hides an added skill file.
    source = tmp_path / "source"
    source.mkdir()
    (source / ".gitignore").write_text("skills/**/SKILL.md\n", encoding="utf-8")
    pinned_sha = commit_source(source)
    monkeypatch.setattr(builder, "SOURCE_SHA", pinned_sha)
    injected = source / "skills" / "injected" / "SKILL.md"
    injected.parent.mkdir(parents=True)
    injected.write_text("Untrusted injected skill\n", encoding="utf-8")
    ordinary_status = subprocess.check_output(
        ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=all"],
        text=True,
    )
    assert ordinary_status == ""

    # When source provenance is verified before packaging.
    with pytest.raises(builder.BuildError, match="clean"):
        builder.verify_source_revision(source)


def test_check_rebuild_detects_coordinated_source_and_notice_tamper(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Given a clean pinned source and a valid generated package.
    source = tmp_path / "source"
    source.mkdir()
    make_productivity_source(source)
    pinned_sha = commit_source(source)
    monkeypatch.setattr(builder, "SOURCE_SHA", pinned_sha)
    monkeypatch.setattr(validator, "PINNED_SOURCE_SHA", pinned_sha)
    output = tmp_path / "plugins"
    builder.build_packages(source, output, ("productivity",))
    package = output / "kw-productivity"
    preserved = package / "skills" / "sample" / "SOURCE.md"
    preserved.write_text(preserved.read_text(encoding="utf-8") + "Tampered instructions.\n", encoding="utf-8")
    notice = package / "NOTICE.md"
    prefix, marker, inventory_text = notice.read_text(encoding="utf-8").partition(builder.INVENTORY_START)
    inventory = json.loads(inventory_text.removesuffix("\n-->\n"))
    inventory["skills/sample/SOURCE.md"] = hashlib.sha256(preserved.read_bytes()).hexdigest()
    notice.write_text(
        prefix + marker + json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n-->\n",
        encoding="utf-8",
    )
    assert validator.validate_packages(output, ("productivity",)) == []
    monkeypatch.setattr(
        sys,
        "argv",
        ["build.py", "--source", str(source), "--output", str(output), "--modules", "productivity", "--check"],
    )

    # When check mode compares the package to a fresh build from pinned source.
    exit_code = builder.main()

    # Then coordinated edits to SOURCE.md and NOTICE.md are rejected.
    assert exit_code != 0
    assert "differs from clean pinned source" in capsys.readouterr().err
