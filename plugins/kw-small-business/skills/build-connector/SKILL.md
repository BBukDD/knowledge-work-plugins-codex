---
name: build-connector
description: "Gets Claude talking to a tool nobody built an official connector for. Works out what the system is, checks the Claude connector directory for an existing connector first, and when there isn't one connects the tool through Zapier — never by hand-building against a raw API — with credentials handled safely and approval gates on anything that writes. This is what turns \"my ERP isn't supported\" into an afternoon. Use this whenever the owner names a tool that isn't connected —…"
---

# build-connector for Codex

Read [SOURCE.md](SOURCE.md) for the full original workflow and its relative supporting files. SOURCE.md is preserved verbatim from the Anthropic project; adapt its task logic to Codex.

## Request and tools

Treat a Claude slash invocation, `$ARGUMENTS`, and positional argument placeholders as the natural-language request and files the user actually supplied. Extract the relevant inputs from this conversation. Ask only for information necessary to complete the task.

Treat `~~category` and similar `~~` tokens as optional connector capability placeholders. Read [CONNECTORS.md](../../CONNECTORS.md) for the Codex capability map. Use only connected Codex tools that are currently available for the requested operation; do not assume a named SaaS service is connected. If no matching connector exists, use user-provided files or public information where appropriate, and state the resulting limitation.

Claude-specific tool names, permissions, and MCP calls in upstream source material do not override current Codex tools or instructions. Do not auto-register MCP servers, start OAuth flows, or run upstream scripts merely because SOURCE.md mentions them. Inspect a supporting script and its inputs before using it for an authorized task.

For consequential external writes such as sending, publishing, changing records, or signing, prepare a concrete reviewable result and act only with user authorization already granted in this request or session; otherwise ask for approval for that action.
