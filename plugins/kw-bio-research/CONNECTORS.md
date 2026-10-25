# Codex capabilities for bio-research

The original connector guide is in [UPSTREAM_CONNECTORS.md](UPSTREAM_CONNECTORS.md) when the source module supplied one. It describes Claude-specific integrations and is reference material, not active Codex configuration.

| Source notation | Codex action |
| --- | --- |
| `/skill ...`, `$ARGUMENTS` | Use the user's natural-language request and attached files. |
| Claude `Read`, `WebFetch`, commands | Use corresponding available Codex file, web, and app tools. |
| `.mcp.json`, OAuth endpoints | No automatic setup; use only already connected, authorized tools. |
| `~~AI` | Look for a currently available Codex connector with AI capabilities; otherwise use supplied files or report the gap. |
| `~~category` | Look for a currently available Codex connector with category capabilities; otherwise use supplied files or report the gap. |
| `~~chemical` | Look for a currently available Codex connector with chemical capabilities; otherwise use supplied files or report the gap. |
| `~~clinical` | Look for a currently available Codex connector with clinical capabilities; otherwise use supplied files or report the gap. |
| `~~data` | Look for a currently available Codex connector with data capabilities; otherwise use supplied files or report the gap. |
| `~~drug` | Look for a currently available Codex connector with drug capabilities; otherwise use supplied files or report the gap. |
| `~~genomics` | Look for a currently available Codex connector with genomics capabilities; otherwise use supplied files or report the gap. |
| `~~journal` | Look for a currently available Codex connector with journal capabilities; otherwise use supplied files or report the gap. |
| `~~lab` | Look for a currently available Codex connector with lab capabilities; otherwise use supplied files or report the gap. |
| `~~literature` | Look for a currently available Codex connector with literature capabilities; otherwise use supplied files or report the gap. |
| `~~scientific` | Look for a currently available Codex connector with scientific capabilities; otherwise use supplied files or report the gap. |
| `~~tool` | Look for a currently available Codex connector with tool capabilities; otherwise use supplied files or report the gap. |

Check the selected tool's actual read/write capability before acting. Original service examples do not prove a Codex connection exists. Obtain user authorization for a consequential external write when it is not already granted in the request or session.
