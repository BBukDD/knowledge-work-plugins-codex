"""Hash-guarded adaptations for the three opt-in upstream helper scripts."""

from __future__ import annotations

import hashlib
from pathlib import Path

FRAGMENTS = Path(__file__).with_name("security_fragments")
SCRIPT_HASHES = {
    "bio-research": {
        "skills/nextflow-development/scripts/utils/ncbi_utils.py": "bfed0a0570f3344036277867c3e69fb6136ae87040ed2640d5b62919a046cfc8",
        "skills/nextflow-development/scripts/sra_geo_fetch.py": "0bd4f292350b47b71e0048a223ca50ebdde0ced1f33d5661daf756c73d1b5a31",
    },
    "data": {
        "skills/data-context-extractor/scripts/package_data_skill.py": "ce79da32ea049db99c91fff0dfcc8ba1ece91940bbbf992de9283cdebe5a4d64",
    },
}


class SecurityOverrideError(ValueError):
    """An upstream script no longer matches its reviewed preimage."""


def _replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SecurityOverrideError(f"Security override anchor missing or repeated: {old[:70]!r}")
    return text.replace(old, new, 1)


def _replace_region(text: str, start: str, end: str, fragment: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise SecurityOverrideError(f"Security override region changed: {start!r}")
    prefix, rest = text.split(start, 1)
    _, suffix = rest.split(end, 1)
    return prefix + (FRAGMENTS / fragment).read_text(encoding="utf-8") + end + suffix


def _adapt(relative: str, original: str) -> str:
    if relative.endswith("/utils/ncbi_utils.py"):
        text = _replace_once(
            original,
            "import json\nimport logging\nimport re\nimport shutil\nimport time\n",
            "import hashlib\nimport json\nimport logging\nimport os\nimport re\nimport tempfile\nimport time\n",
        )
        text = _replace_once(
            text,
            "from urllib.request import Request, urlopen\n",
            "from urllib.parse import unquote, urlsplit, urlunsplit\n"
            "from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen\n",
        )
        return _replace_region(text, "def fetch_ena_fastq_urls(", "def fetch_pubmed_metadata(", "ncbi_download.pyfrag")
    if relative.endswith("/sra_geo_fetch.py"):
        text = _replace_once(
            original, "from typing import Dict, List, Optional, Tuple\n", "from typing import Dict, List, Optional\n"
        )
        text = _replace_region(
            text, "def download_fastq_file(", "def interactive_select_group(", "sra_download_helper.pyfrag"
        )
        return _replace_region(
            text, "    # Check for existing files\n", "    # Save metadata\n", "sra_download_body.pyfrag"
        )
    if relative.endswith("/package_data_skill.py"):
        text = _replace_once(original, "import sys\nimport zipfile\n", "import os\nimport sys\nimport tempfile\nimport zipfile\n")
        return _replace_region(text, "def package_skill(", "def main():", "package_skill.pyfrag")
    raise SecurityOverrideError(f"Unrecognized security override path: {relative}")


def apply_security_overrides(source_module: Path, target_package: Path, module_name: str) -> tuple[str, ...]:
    """Patch reviewed copies only after checking exact upstream source bytes."""
    scripts = SCRIPT_HASHES.get(module_name, {})
    adapted: list[str] = []
    for relative, expected_sha in scripts.items():
        source_bytes = (source_module / relative).read_bytes()
        actual_sha = hashlib.sha256(source_bytes).hexdigest()
        if actual_sha != expected_sha:
            raise SecurityOverrideError(
                f"Upstream script preimage changed for {relative}: expected {expected_sha}, found {actual_sha}"
            )
        target = target_package / relative
        if target.read_bytes() != source_bytes:
            raise SecurityOverrideError(f"Copied script differs from pinned preimage: {relative}")
        target.write_text(_adapt(relative, source_bytes.decode("utf-8")), encoding="utf-8")
        adapted.append(relative)
    return tuple(adapted)
