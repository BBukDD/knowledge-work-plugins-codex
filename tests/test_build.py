from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools import build as build_module
from tools.build import BuildError, build_packages
from tools.render import render_connectors
from tools.validate import marketplace_errors, source_link_warnings, validate_packages

BUILDER = Path(__file__).resolve().parents[1] / "tools" / "build.py"


def make_module(root: Path, name: str) -> Path:
    module = root / name
    (module / ".claude-plugin").mkdir(parents=True)
    (module / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": name,
                "description": f"Source {name} capability",
                "author": {"name": "Anthropic"},
            }
        ),
        encoding="utf-8",
    )
    (module / "LICENSE").write_text("Apache License fixture\n", encoding="utf-8")
    return module


def make_skill(module: Path, name: str, description: str, body: str) -> None:
    skill = module / "skills" / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n{body}\n",
        encoding="utf-8",
    )


def run_builder(source: Path, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--source",
            str(source),
            "--output",
            str(output),
            *extra,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_build_preserves_plain_connector_script_command_and_cross_link(
    tmp_path: Path,
) -> None:
    # Given a first-party module with every supported resource class.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "plain", "Write a plain report.", "See [shared](../../shared/voice.md).")
    make_skill(module, "connected", "Use ~~crm if available.", "Run /connected $ARGUMENTS.")
    (module / "shared").mkdir()
    (module / "shared" / "voice.md").write_text("House voice\n", encoding="utf-8")
    (module / "scripts").mkdir()
    (module / "scripts" / "prepare.py").write_text("print('preserved')\n", encoding="utf-8")
    (module / "commands").mkdir()
    (module / "commands" / "review.md").write_text(
        "---\ndescription: Review an artifact\n---\n\nUse $ARGUMENTS.\n", encoding="utf-8"
    )
    (module / "CONNECTORS.md").write_text("Original ~~crm connector\n", encoding="utf-8")
    (module / ".mcp.json").write_text('{"mcpServers": {}}\n', encoding="utf-8")
    output = tmp_path / "plugins"

    # When the builder packages that explicit module.
    skill_count, command_count = build_packages(source, output, ("productivity",))

    # Then source references survive and Codex entrypoints replace Claude entrypoints.
    assert (skill_count, command_count) == (2, 1)
    package = output / "kw-productivity"
    manifest = json.loads((package / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "kw-productivity"
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert "Unofficial Codex adaptation" in manifest["description"]
    assert manifest["license"] == "Apache-2.0"
    assert manifest["repository"].startswith("https://github.com/anthropics/")
    assert (package / "skills" / "plain" / "SOURCE.md").read_text(encoding="utf-8") == (
        module / "skills" / "plain" / "SKILL.md"
    ).read_text(encoding="utf-8")
    wrapper = (package / "skills" / "connected" / "SKILL.md").read_text(encoding="utf-8")
    assert wrapper.startswith("---\nname: connected\ndescription:")
    assert "[SOURCE.md](SOURCE.md)" in wrapper
    assert "$ARGUMENTS" in wrapper and "~~" in wrapper
    assert "Codex" in wrapper and "authorization" in wrapper
    assert (package / "skills" / "plain" / "../../shared/voice.md").is_file()
    assert (package / "scripts" / "prepare.py").is_file()
    assert (package / "UPSTREAM_CONNECTORS.md").read_text(encoding="utf-8") == "Original ~~crm connector\n"
    assert "33d3dea41a341b341d4f5da2e8801ae0c89be2b8" in (
        package / "NOTICE.md"
    ).read_text(encoding="utf-8")
    assert "~~crm" in (package / "CONNECTORS.md").read_text(encoding="utf-8")
    assert (package / "skills" / "command-review" / "SKILL.md").is_file()
    assert "[review.md](../../commands/review.md)" in (
        package / "skills" / "command-review" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert not list(package.rglob(".mcp.json"))
    assert not list(package.rglob(".claude-plugin"))


def test_special_modules_route_to_codex_native_capabilities(tmp_path: Path) -> None:
    # Given two source modules with Claude-specific tool workflows.
    source = tmp_path / "source"
    source.mkdir()
    pdf = make_module(source, "pdf-viewer")
    make_skill(pdf, "view-pdf", "View a PDF.", "Call display_pdf on $ARGUMENTS.")
    cowork = make_module(source, "cowork-plugin-management")
    make_skill(cowork, "create-cowork-plugin", "Create a plugin.", "Edit .claude-plugin files.")
    output = tmp_path / "plugins"

    # When they are packaged together.
    skill_count, command_count = build_packages(
        source, output, ("pdf-viewer", "cowork-plugin-management")
    )

    # Then Codex-native routes are explicit before the untouched source material.
    assert (skill_count, command_count) == (2, 0)
    pdf_wrapper = (output / "kw-pdf-viewer" / "skills" / "view-pdf" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    cowork_wrapper = (
        output / "kw-cowork-plugin-management" / "skills" / "create-cowork-plugin" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Codex PDF" in pdf_wrapper
    assert "display_pdf" in pdf_wrapper and "not a native Codex tool" in pdf_wrapper
    assert "Codex plugin.json" in cowork_wrapper
    assert "skill-creator" in cowork_wrapper
    assert "Cowork mode" not in cowork_wrapper.split("---", maxsplit=2)[1]


def test_missing_module_license_uses_clean_adapter_license(tmp_path: Path) -> None:
    # Given a first-party module that inherits the upstream root license.
    source = tmp_path / "source"
    source.mkdir()
    (source / "LICENSE").write_text("Apache License fixture with stray draft\n", encoding="utf-8")
    module = make_module(source, "operations")
    (module / "LICENSE").unlink()
    make_skill(module, "sample", "Use a sample workflow.", "Follow the source.")
    output = tmp_path / "plugins"

    # When the module is packaged for Codex.
    build_packages(source, output, ("operations",))

    # Then the distributable carries the standard license and records the substitution.
    package = output / "kw-operations"
    adapter_license = BUILDER.parents[1] / "LICENSE"
    assert (package / "LICENSE").read_bytes() == adapter_license.read_bytes()
    assert "standard Apache-2.0 text" in (package / "NOTICE.md").read_text(encoding="utf-8")


def test_build_is_deterministic_and_validation_detects_forbidden_manifest(tmp_path: Path) -> None:
    # Given one valid source module.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "plain", "Write a report.", "Write a report.")
    output = tmp_path / "plugins"

    # When the builder runs twice on the same source.
    first = build_packages(source, output, ("productivity",))
    first_digest = hashlib.sha256(
        b"".join(path.read_bytes() for path in sorted(output.rglob("*")) if path.is_file())
    ).hexdigest()
    second = build_packages(source, output, ("productivity",))
    second_digest = hashlib.sha256(
        b"".join(path.read_bytes() for path in sorted(output.rglob("*")) if path.is_file())
    ).hexdigest()

    # Then the output is byte-for-byte stable and safety validation catches regression.
    assert first == second == (1, 0)
    assert first_digest == second_digest
    assert validate_packages(output, ("productivity",)) == []
    (output / "kw-productivity" / ".mcp.json").write_text("{}", encoding="utf-8")
    assert any("forbidden" in error for error in validate_packages(output, ("productivity",)))


def test_connector_tokens_with_equal_casefold_sort_deterministically() -> None:
    # Given source tokens that differ only by case.
    source = "Use ~~task and ~~Task."

    # When the connector guide is rendered.
    guide = render_connectors("productivity", source, [])

    # Then the exact-case tie break is stable.
    assert guide.index("| `~~Task` |") < guide.index("| `~~task` |")


def test_partner_built_cannot_be_explicitly_bundled(tmp_path: Path) -> None:
    # Given a partner directory with a plausible manifest.
    source = tmp_path / "source"
    source.mkdir()
    make_module(source, "partner-built")

    # When a caller names it as an explicit module.
    result = run_builder(source, tmp_path / "plugins", "--modules", "partner-built")

    # Then no package is emitted.
    assert result.returncode != 0
    assert "Not a permitted first-party module" in result.stderr
    assert not (tmp_path / "plugins" / "kw-partner-built").exists()


def test_cli_rejects_unpinned_source_before_writing(tmp_path: Path) -> None:
    # Given a plausible source module outside the pinned Git checkout.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "plain", "Write a report.", "Write a report.")
    output = tmp_path / "plugins"

    # When the user-facing CLI is run against it.
    result = run_builder(source, output, "--modules", "productivity")

    # Then source provenance is enforced before any package is written.
    assert result.returncode != 0
    assert "pinned commit" in result.stderr
    assert not output.exists()


def test_failed_rebuild_preserves_previous_package(tmp_path: Path) -> None:
    # Given an already generated package and a source module that later becomes invalid.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "plain", "Write a report.", "Write a report.")
    output = tmp_path / "plugins"
    build_packages(source, output, ("productivity",))
    original = (output / "kw-productivity" / "skills" / "plain" / "SOURCE.md").read_bytes()
    (module / "skills" / "plain" / "SKILL.md").unlink()

    # When a rebuild fails during staging.
    with pytest.raises(BuildError, match="No source skills"):
        build_packages(source, output, ("productivity",))

    # Then the existing valid package remains intact.
    assert (output / "kw-productivity" / "skills" / "plain" / "SOURCE.md").read_bytes() == original


def test_marketplace_mapping_and_upstream_links_are_audited(tmp_path: Path) -> None:
    # Given one local marketplace entry and source Markdown with a broken local link.
    project = tmp_path / "project"
    marketplace_dir = project / ".agents" / "plugins"
    marketplace_dir.mkdir(parents=True)
    marketplace_dir.joinpath("marketplace.json").write_text(
        json.dumps({"plugins": [{"name": "kw-productivity", "source": {"source": "local", "path": "./plugins/wrong"}}]}),
        encoding="utf-8",
    )
    package = project / "plugins" / "kw-productivity"
    package.mkdir(parents=True)
    (package / "UPSTREAM_README.md").write_text(
        "See [missing](reference/missing.md), [parent](../missing.md), and "
        "[external](design.canva.ai/...).\n",
        encoding="utf-8",
    )

    # When the local install route and preserved source links are audited.
    mapping_errors = marketplace_errors(project, ("productivity",))
    link_warnings = source_link_warnings(package)

    # Then the wrong install path and genuine local gap are reported separately.
    assert any("wrong local source" in error for error in mapping_errors)
    assert len(link_warnings) == 2
    assert any("reference/missing.md" in warning for warning in link_warnings)
    assert any("../missing.md" in warning for warning in link_warnings)


@pytest.mark.parametrize(
    ("module_name", "upstream_claim", "codex_capability", "unsupported_claim"),
    [
        ("cowork-plugin-management", "Configure MCP servers and ask Claude.", "Codex plugins and skills", "Configure MCP servers"),
        ("pdf-viewer", "Use a live interactive viewer and download annotated PDFs.", "available Codex PDF", "live interactive viewer"),
        ("small-business", "Install and ask Claude to onboard you.", "available connectors", "ask Claude"),
        ("productivity", "Syncs with your calendar, email, and chat.", "available connected tools", "Syncs with"),
    ],
)
def test_manifest_copy_describes_codex_capability_without_upstream_promises(
    tmp_path: Path,
    module_name: str,
    upstream_claim: str,
    codex_capability: str,
    unsupported_claim: str,
) -> None:
    # Given an upstream module description that claims a Claude-only or automatic capability.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, module_name)
    manifest_path = module / ".claude-plugin" / "plugin.json"
    original_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    original_manifest["description"] = upstream_claim
    manifest_path.write_text(json.dumps(original_manifest), encoding="utf-8")
    make_skill(module, "sample", "Work with this module.", "Use supplied information.")
    output = tmp_path / "plugins"

    # When the Codex package is built.
    build_packages(source, output, (module_name,))

    # Then its marketplace copy states the conditional Codex capability without the false promise.
    description = json.loads(
        (output / f"kw-{module_name}" / "plugin.json").read_text(encoding="utf-8")
    )["description"]
    assert codex_capability in description
    assert unsupported_claim not in description


def test_validator_rejects_broken_generated_connector_link(tmp_path: Path) -> None:
    # Given a valid generated wrapper whose connector target is then changed to a missing file.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "sample", "Use the sample workflow.", "Follow the source.")
    output = tmp_path / "plugins"
    build_packages(source, output, ("productivity",))
    wrapper = output / "kw-productivity" / "skills" / "sample" / "SKILL.md"
    wrapper.write_text(
        wrapper.read_text(encoding="utf-8").replace(
            "../../CONNECTORS.md", "../../qa-missing-connectors.md"
        ),
        encoding="utf-8",
    )

    # When generated packages are validated after the edit.
    errors = validate_packages(output, ("productivity",))

    # Then the unresolved generated link is a validation error.
    assert any("qa-missing-connectors.md" in error for error in errors)


def test_subset_rebuild_validates_existing_allowlisted_packages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given an output with two valid first-party packages.
    source = tmp_path / "source"
    source.mkdir()
    for module_name in ("productivity", "operations"):
        module = make_module(source, module_name)
        make_skill(module, "sample", "Use the sample workflow.", "Follow the source.")
    output = tmp_path / "plugins"
    build_packages(source, output, ("productivity", "operations"))
    monkeypatch.setattr(build_module, "verify_source_revision", lambda _source: None)
    monkeypatch.setattr(
        sys,
        "argv",
        ["build.py", "--source", str(source), "--output", str(output), "--modules", "productivity"],
    )

    # When one module is rebuilt through the CLI entrypoint.
    result = build_module.main()

    # Then both installed packages remain part of validation and the subset build succeeds.
    assert result == 0
    assert validate_packages(output, ("productivity", "operations")) == []


def test_check_mode_requires_pinned_source(tmp_path: Path) -> None:
    # Given a generated package but an unpinned source checkout.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "sample", "Use the sample workflow.", "Follow the source.")
    output = tmp_path / "plugins"
    build_packages(source, output, ("productivity",))

    # When the CLI checks the package against that source.
    result = run_builder(source, output, "--modules", "productivity", "--check")

    # Then provenance is rejected rather than silently marked valid.
    assert result.returncode != 0
    assert "pinned commit" in result.stderr


def test_validator_rejects_wrong_revision(tmp_path: Path) -> None:
    # Given a valid generated package.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "sample", "Use the sample workflow.", "Follow the source.")
    output = tmp_path / "plugins"
    build_packages(source, output, ("productivity",))
    package = output / "kw-productivity"
    manifest_path = package / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    original_url = manifest["repository"]

    # When the pinned source URL is changed to another revision.
    manifest["repository"] = original_url.replace(
        "33d3dea41a341b341d4f5da2e8801ae0c89be2b8", "0000000000000000000000000000000000000000"
    )
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    # Then the validator rejects the package provenance.
    assert any("pinned" in error for error in validate_packages(output, ("productivity",)))


def test_validator_rejects_tampered_marker(tmp_path: Path) -> None:
    # Given a valid generated package.
    source = tmp_path / "source"
    source.mkdir()
    module = make_module(source, "productivity")
    make_skill(module, "sample", "Use the sample workflow.", "Follow the source.")
    output = tmp_path / "plugins"
    build_packages(source, output, ("productivity",))
    package = output / "kw-productivity"

    # When the generator marker is altered.
    (package / ".codex-adapter-generated").write_text("tampered\n", encoding="utf-8")

    # Then the marker mismatch is reported.
    assert any("marker" in error for error in validate_packages(output, ("productivity",)))
