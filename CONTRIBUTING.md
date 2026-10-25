# Contributing

Thanks for helping improve this unofficial Codex adaptation. Start with a focused issue or pull request that describes the workflow or bug, the module affected, and how you verified the change. For a security issue, use the private route in [SECURITY.md](SECURITY.md).

## Before editing

- Read [README.md](README.md), [CATALOG.md](CATALOG.md), and [tools/README.md](tools/README.md) for the supported scope.
- The generated `plugins/kw-*` packages come from [Anthropic's upstream repository](https://github.com/anthropics/knowledge-work-plugins) at commit `33d3dea41a341b341d4f5da2e8801ae0c89be2b8`. Change the adapter under `tools/` and regenerate packages rather than editing generated wrappers or inventories by hand.
- Keep original workflow text and attribution intact. Five modules without a standalone upstream license use this repository's clean standard Apache-2.0 text; keep their package notices consistent with that substitution. Do not add partner-built modules, external marketplace repositories, or SaaS connections without reviewing each one's license, provenance, permissions, and behavior.

## Build and test

Use Python 3.11 or newer and a clean checkout of the pinned upstream commit. The upstream checkout must have no modified, untracked, or ignored files:

```sh
git clone https://github.com/anthropics/knowledge-work-plugins.git /tmp/knowledge-work-plugins-source
git -C /tmp/knowledge-work-plugins-source checkout 33d3dea41a341b341d4f5da2e8801ae0c89be2b8
python3.11 tools/build.py --source /tmp/knowledge-work-plugins-source --output plugins
python3.11 tools/build.py --source /tmp/knowledge-work-plugins-source --output plugins --check
python3.11 tools/validate.py --project .
```

Run the offline test suite with `pytest` available in your Python 3.11 environment:

```sh
python3.11 -m pytest -q tests
```

The first build regenerates the tracked plugin packages; `--check` then compares every delivered file with a fresh build. Review the complete generated diff before opening a pull request. If you change a Skill entry or install behavior, also test it in a separate Codex configuration with `codex plugin marketplace add` and `codex plugin add`; do not use your primary installation as a test fixture. [QA_REPORT.md](QA_REPORT.md) records the checks performed for the initial release.

## Updating the upstream pin

Treat a new upstream commit as a new import. Inspect changes to licenses, authorship, scripts, commands, references, MCP configuration, and the marketplace inventory before changing the pin or any allowlist. Reassess the three security adaptations against the new original script hashes, regenerate packages, update counts and attribution where needed, and run the build comparison, validator, and tests. Describe any behavior that Codex still cannot reproduce.

This project is not affiliated with Anthropic or OpenAI. Keep pull request descriptions factual about which behavior is adapted and which requires an existing Codex connection.
