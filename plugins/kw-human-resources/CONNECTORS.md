# Codex capabilities for human-resources

The original connector guide is in [UPSTREAM_CONNECTORS.md](UPSTREAM_CONNECTORS.md) when the source module supplied one. It describes Claude-specific integrations and is reference material, not active Codex configuration.

| Source notation | Codex action |
| --- | --- |
| `/skill ...`, `$ARGUMENTS` | Use the user's natural-language request and attached files. |
| Claude `Read`, `WebFetch`, commands | Use corresponding available Codex file, web, and app tools. |
| `.mcp.json`, OAuth endpoints | No automatic setup; use only already connected, authorized tools. |
| `~~ATS` | Look for a currently available Codex connector with ATS capabilities; otherwise use supplied files or report the gap. |
| `~~calendar` | Look for a currently available Codex connector with calendar capabilities; otherwise use supplied files or report the gap. |
| `~~category` | Look for a currently available Codex connector with category capabilities; otherwise use supplied files or report the gap. |
| `~~chat` | Look for a currently available Codex connector with chat capabilities; otherwise use supplied files or report the gap. |
| `~~compensation` | Look for a currently available Codex connector with compensation capabilities; otherwise use supplied files or report the gap. |
| `~~email` | Look for a currently available Codex connector with email capabilities; otherwise use supplied files or report the gap. |
| `~~HRIS` | Look for a currently available Codex connector with HRIS capabilities; otherwise use supplied files or report the gap. |
| `~~knowledge` | Look for a currently available Codex connector with knowledge capabilities; otherwise use supplied files or report the gap. |
| `~~project` | Look for a currently available Codex connector with project capabilities; otherwise use supplied files or report the gap. |

Check the selected tool's actual read/write capability before acting. Original service examples do not prove a Codex connection exists. Obtain user authorization for a consequential external write when it is not already granted in the request or session.
