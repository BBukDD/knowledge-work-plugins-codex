# Codex capabilities for customer-support

The original connector guide is in [UPSTREAM_CONNECTORS.md](UPSTREAM_CONNECTORS.md) when the source module supplied one. It describes Claude-specific integrations and is reference material, not active Codex configuration.

| Source notation | Codex action |
| --- | --- |
| `/skill ...`, `$ARGUMENTS` | Use the user's natural-language request and attached files. |
| Claude `Read`, `WebFetch`, commands | Use corresponding available Codex file, web, and app tools. |
| `.mcp.json`, OAuth endpoints | No automatic setup; use only already connected, authorized tools. |
| `~~category` | Look for a currently available Codex connector with category capabilities; otherwise use supplied files or report the gap. |
| `~~chat` | Look for a currently available Codex connector with chat capabilities; otherwise use supplied files or report the gap. |
| `~~cloud` | Look for a currently available Codex connector with cloud capabilities; otherwise use supplied files or report the gap. |
| `~~CRM` | Look for a currently available Codex connector with CRM capabilities; otherwise use supplied files or report the gap. |
| `~~email` | Look for a currently available Codex connector with email capabilities; otherwise use supplied files or report the gap. |
| `~~knowledge` | Look for a currently available Codex connector with knowledge capabilities; otherwise use supplied files or report the gap. |
| `~~project` | Look for a currently available Codex connector with project capabilities; otherwise use supplied files or report the gap. |
| `~~support` | Look for a currently available Codex connector with support capabilities; otherwise use supplied files or report the gap. |

Check the selected tool's actual read/write capability before acting. Original service examples do not prove a Codex connection exists. Obtain user authorization for a consequential external write when it is not already granted in the request or session.
