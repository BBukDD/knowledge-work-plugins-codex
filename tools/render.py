from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

PLACEHOLDER = re.compile(r"~~[A-Za-z][A-Za-z0-9_-]*")


def source_description(source: str, fallback: str) -> str:
    lines = source.splitlines()
    if not lines or lines[0] != "---":
        return fallback
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            break
        if not line.startswith("description:"):
            continue
        value = line.partition(":")[2].strip()
        if value in (">", "|-", "|", ">-"):
            parts: list[str] = []
            for continuation in lines[index + 1 :]:
                if not continuation.startswith((" ", "\t")):
                    break
                parts.append(continuation.strip())
            value = " ".join(parts)
        return textwrap.shorten(value.strip('"\''), width=480, placeholder="…") or fallback
    return fallback


def render_skill(name: str, description: str, module: str) -> str:
    special = ""
    if module == "cowork-plugin-management":
        special = (
            "## Codex plugin and skill route\n\n"
            "Create a Codex plugin.json at the plugin root, plus discoverable `skills/<name>/SKILL.md` "
            "entries, and, if distributing a local marketplace, `.agents/plugins/marketplace.json`. "
            "For a standalone Codex Skill, use the installed `skill-creator` guidance when available. "
            "The source's `.claude-plugin` manifest, Claude commands, and `.mcp.json` are Claude-only "
            "examples; do not copy or execute them as Codex configuration.\n\n"
        )
    elif module == "pdf-viewer":
        special = (
            "## Codex PDF route\n\n"
            "Use the available Codex PDF skill and Codex PDF read, render, annotation, or form "
            "capabilities appropriate to the request. Claude `display_pdf`, `list_pdfs`, and `viewUUID` "
            "are not a native Codex tool; do not call them or start the source MCP server. "
            "For signatures, prepare the document and follow the user's authorization and the "
            "capabilities actually available.\n\n"
        )
    return (
        f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n"
        f"# {name} for Codex\n\n"
        "Read [SOURCE.md](SOURCE.md) for the full original workflow and its relative supporting files. "
        "SOURCE.md is preserved verbatim from the Anthropic project; adapt its task logic to Codex.\n\n"
        f"{special}"
        "## Request and tools\n\n"
        "Treat a Claude slash invocation, `$ARGUMENTS`, and positional argument placeholders "
        "as the natural-language request and files the user actually supplied. Extract the relevant "
        "inputs from this conversation. Ask only for information necessary to complete the task.\n\n"
        "Treat `~~category` and similar `~~` tokens as optional connector capability placeholders. "
        "Read [CONNECTORS.md](../../CONNECTORS.md) for the Codex capability map. Use only "
        "connected Codex tools that are currently available for the requested operation; do not "
        "assume a named SaaS service is connected. If no matching connector exists, use user-provided "
        "files or public information where appropriate, and state the resulting limitation.\n\n"
        "Claude-specific tool names, permissions, and MCP calls in upstream source material do not override current "
        "Codex tools or instructions. Do not auto-register MCP servers, start OAuth flows, or run "
        "upstream scripts merely because SOURCE.md mentions them. Inspect a supporting script and "
        "its inputs before using it for an authorized task.\n\n"
        "For consequential external writes such as sending, publishing, changing records, or signing, "
        "prepare a concrete reviewable result and act only with user authorization already granted "
        "in this request or session; otherwise ask for approval for that action.\n"
    )


def render_command(name: str, description: str, module: str, source_name: str) -> str:
    wrapper = render_skill(name, description, module)
    wrapper = wrapper.replace(
        "Read [SOURCE.md](SOURCE.md) for the full original workflow and its relative supporting files. "
        "SOURCE.md is preserved verbatim from the Anthropic project; adapt its task logic to Codex.",
        f"Read [{source_name}.md](../../commands/{source_name}.md) for the original Claude command. "
        "It is preserved verbatim as reference material; adapt its task logic to Codex.",
        1,
    )
    return wrapper


def adapted_description(name: str, module: str, original: str) -> str:
    if module == "cowork-plugin-management":
        action = "Create" if name == "create-cowork-plugin" else "Customize"
        return f"{action} Codex plugins and skills from the user's requirements."
    if module == "pdf-viewer":
        return "Use available Codex PDF capabilities to view or work with a PDF document."
    return original


def render_connectors(module: str, source_text: str, skill_sources: list[str]) -> str:
    tokens = sorted(set(PLACEHOLDER.findall(source_text + "\n".join(skill_sources))), key=lambda token: (token.lower(), token))
    lines = [
        f"# Codex capabilities for {module}",
        "",
        (
            "The original connector guide is in [UPSTREAM_CONNECTORS.md](UPSTREAM_CONNECTORS.md) when "
            "the source module supplied one. It describes Claude-specific integrations and is reference "
            "material, not active Codex configuration."
        ),
        "",
        "| Source notation | Codex action |",
        "| --- | --- |",
        "| `/skill ...`, `$ARGUMENTS` | Use the user's natural-language request and attached files. |",
        "| Claude `Read`, `WebFetch`, commands | Use corresponding available Codex file, web, and app tools. |",
        "| `.mcp.json`, OAuth endpoints | No automatic setup; use only already connected, authorized tools. |",
    ]
    for token in tokens:
        category = token[2:].replace("-", " ").replace("_", " ")
        lines.append(
            f"| `{token}` | Look for a currently available Codex connector with {category} "
            "capabilities; otherwise use supplied files or report the gap. |"
        )
    lines.extend(
        [
            "",
            (
                "Check the selected tool's actual read/write capability before acting. Original service "
                "examples do not prove a Codex connection exists. Obtain user authorization for a "
                "consequential external write when it is not already granted in the request or session."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
