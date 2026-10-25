# Attribution and changes

This repository is an unofficial Codex adaptation of Anthropic's
[Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins)
at commit `33d3dea41a341b341d4f5da2e8801ae0c89be2b8`.
It is not published or endorsed by Anthropic or OpenAI.

The 17 bundled first-party modules include Anthropic-authored workflows and
reference files. Their original skill text is preserved as `SOURCE.md`; the
generated `SKILL.md` entry points, plugin manifests, and connector guidance
adapt those workflows for Codex. Five upstream commands are also exposed as
Codex skills. The original module and command paths are recorded in each
plugin's `NOTICE.md` and in [CATALOG.md](CATALOG.md).

The root [LICENSE](LICENSE) contains the standard Apache License 2.0 text.
The pinned upstream root `LICENSE` has unrelated draft text appended after
the standard license. Five first-party modules inherit that root license;
their generated packages use the clean standard text and say so in their
`NOTICE.md`. The remaining modules retain their own upstream license files.

Three optional Python helper scripts have reviewed safety changes. Their
paths and package hashes are listed in the affected plugins' `NOTICE.md`;
the build tool checks the original scripts' hashes before applying changes.
Partner-built modules and external marketplaces are excluded.
