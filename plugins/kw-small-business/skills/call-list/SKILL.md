---
name: call-list
description: "Builds today's call list. Runs lead-triage to rank the top-5 leads most worth calling, supplies talking points from email history, blocks time on the calendar, and drafts follow-up messages. Trigger on \"call list,\" \"who am I calling today,\" \"top five to call today,\" or \"block time for calls.\" An owner who wants leads scored or ranked with no calendar blocks routes to lead-triage directly. Accepts optional count and date arguments."
---

# call-list for Codex

Read [SOURCE.md](SOURCE.md) for the full original workflow and its relative supporting files. SOURCE.md is preserved verbatim from the Anthropic project; adapt its task logic to Codex.

## Request and tools

Treat a Claude slash invocation, `$ARGUMENTS`, and positional argument placeholders as the natural-language request and files the user actually supplied. Extract the relevant inputs from this conversation. Ask only for information necessary to complete the task.

Treat `~~category` and similar `~~` tokens as optional connector capability placeholders. Read [CONNECTORS.md](../../CONNECTORS.md) for the Codex capability map. Use only connected Codex tools that are currently available for the requested operation; do not assume a named SaaS service is connected. If no matching connector exists, use user-provided files or public information where appropriate, and state the resulting limitation.

Claude-specific tool names, permissions, and MCP calls in upstream source material do not override current Codex tools or instructions. Do not auto-register MCP servers, start OAuth flows, or run upstream scripts merely because SOURCE.md mentions them. Inspect a supporting script and its inputs before using it for an authorized task.

For consequential external writes such as sending, publishing, changing records, or signing, prepare a concrete reviewable result and act only with user authorization already granted in this request or session; otherwise ask for approval for that action.
