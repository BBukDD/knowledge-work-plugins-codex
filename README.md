# Knowledge Work Plugins for Codex

An **unofficial, opt-in Codex adaptation** of the first-party workflows in [Anthropic's Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins). Install the work area you need without enabling the whole collection. This repository is maintained independently and is **not an Anthropic or OpenAI release**.

[简体中文](README.zh-CN.md) · [Plugin catalog](CATALOG.md) · [Validation record](QA_REPORT.md)

## Quick start

You need a Codex CLI version with the `codex plugin` command. The immutable commit below is the source of release `v0.1.0`. Add that GitHub marketplace revision, inspect its available modules, then install one:

```sh
codex plugin marketplace add BBukDD/knowledge-work-plugins-codex --ref 2f56268419bb84285bcfbfb1f61cdb1afeb0668f
codex plugin list --available
codex plugin add kw-operations@knowledge-work-codex
```

Replace `kw-operations` with any module in the [catalog](CATALOG.md), such as `kw-marketing` or `kw-product-management`. Start a new Codex chat after installation to use the selected skills. Installation does not connect Slack, CRM, email, cloud storage, or any other service.

To inspect the source locally before adding it, check out the same commit:

```sh
git clone https://github.com/BBukDD/knowledge-work-plugins-codex.git
cd knowledge-work-plugins-codex
git checkout 2f56268419bb84285bcfbfb1f61cdb1afeb0668f
codex plugin marketplace add "$(pwd)"
```

## What this repository contains

- **17 independent Codex plugins** containing **181 adapted entries** for the upstream skills and **5 additional skills** converted from Claude commands: four PDF commands and one product brainstorming command.
- A Codex `SKILL.md` entry for each workflow. The original skill text remains in its `SOURCE.md`; reference files and relative paths are preserved. Converted command sources remain in `commands/*.md`.
- A reproducible builder and validator pinned to upstream commit [`33d3dea41a341b341d4f5da2e8801ae0c89be2b8`](https://github.com/anthropics/knowledge-work-plugins/commit/33d3dea41a341b341d4f5da2e8801ae0c89be2b8), plus offline tests.

The [catalog](CATALOG.md) lists every module and explains differences from the Claude implementation. For example, after installing `kw-product-management`, you can ask Codex to organize interview notes into product requirements and identify assumptions to validate.

## Capability and safety boundaries

This release packages the 17 Anthropic first-party modules from the pinned commit. It excludes the five independently authored `partner-built/` modules and marketplace entries that point to other repositories. It does **not** import Claude `.mcp.json` files, register MCP servers, run setup scripts during installation, or bundle account connections. Marketplace metadata marks authentication as `ON_USE`; these packages themselves have no server configuration and require no OAuth during installation.

Upstream placeholders such as `~~chat` and `~~CRM` describe needed capabilities. A workflow can access a real service only when your Codex environment already has a suitable connection and you authorize its use. Otherwise, provide files or text, or ask for a draft based solely on the material at hand. Claude-only PDF viewer behavior and Cowork plugin controls cannot be reproduced exactly; the adapted entries use available Codex capabilities and should state their limits. Instructions in preserved upstream text do not expand your authorization for financial, legal, personnel, payment, or publishing actions.

Some bio-research and data skills include optional Python helpers. They are **not run at install time**. Three helpers were adapted to restrict ENA downloads to designated HTTPS hosts, validate completed downloads and caches, and reject ZIP inputs that resolve outside the selected directory. The builder verifies their pinned upstream hashes before applying those changes. Package `NOTICE.md` files record provenance and file hashes. Those hashes detect accidental changes; they are not a digital signature. See [the validation record](QA_REPORT.md) for tested behavior and remaining limits.

## Build and verify

Use Python 3.11 or newer. The distributed repository contains the adapter and generated plugins, but not a copy of the upstream Git checkout. To verify the generated packages against the exact source:

```sh
git clone https://github.com/anthropics/knowledge-work-plugins.git /tmp/knowledge-work-plugins-source
git -C /tmp/knowledge-work-plugins-source checkout 33d3dea41a341b341d4f5da2e8801ae0c89be2b8
python3.11 tools/build.py --source /tmp/knowledge-work-plugins-source --output plugins --check
python3.11 tools/validate.py --project .
```

The source checkout must be clean, including no untracked or ignored files. `build.py --check` regenerates packages in a temporary directory and compares every path and hash, including `NOTICE.md`. `validate.py` checks the delivered structure and its own file inventory; alone, it does not establish provenance. See [tools/README.md](tools/README.md) for rebuilding and running tests, and [CONTRIBUTING.md](CONTRIBUTING.md) for changes to the adapter.

## Attribution and license

The original workflows are by Anthropic and remain attributed in each module's `NOTICE.md`. This adaptation retains their source material and licenses the adapter under Apache-2.0; see [LICENSE](LICENSE) and the root [NOTICE.md](NOTICE.md) for provenance and license normalization. No endorsement by Anthropic or OpenAI is implied. For vulnerability reports, see [SECURITY.md](SECURITY.md).
