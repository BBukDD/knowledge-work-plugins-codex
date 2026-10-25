# Build and validation tools

Use Python 3.11 or newer. From the project root, package the clean upstream checkout at commit
`33d3dea41a341b341d4f5da2e8801ae0c89be2b8`:

```bash
uv run --no-project --python 3.11 python tools/build.py --source /path/to/knowledge-work-plugins --output plugins
uv run --no-project --python 3.11 python tools/validate.py --project .
```

The builder emits only the 17 allowlisted first-party modules. It stages and validates packages before replacing previously generated `kw-*` directories. It refuses to replace a directory without its generator marker. It never modifies the marketplace manifest or any other project-root file. It copies supporting resources, but does not run upstream scripts or configure MCP/OAuth.

Five upstream modules have no standalone `LICENSE` and inherit the upstream root license, whose standard Apache-2.0 text is followed by unrelated draft text. The builder packages the clean standard text from this repository's root `LICENSE` for those five modules and records that substitution in each package `NOTICE.md`.

Three opt-in upstream Python helpers receive security adaptations during the staged build: `ncbi_utils.py` and `sra_geo_fetch.py` in `kw-bio-research`, and `package_data_skill.py` in `kw-data`. `security_overrides.py` checks the SHA256 preimage of each source script before applying the exact reviewed replacement fragments under `security_fragments/`. A changed upstream script stops the build, even if its containing module is otherwise valid. The original skill text stays in `SOURCE.md`; each affected package `NOTICE.md` names its adapted helper scripts.

Each generated `NOTICE.md` also records a sorted SHA256 inventory for every other package file. The validator compares file names and hashes to catch accidental changes to preserved sources, wrappers, or runnable scripts. It also flags unlisted runtime files such as `__pycache__`; remove those before validating a package for distribution. This inventory is a structural integrity check, **not a cryptographic signature**: someone able to edit a package and its NOTICE can replace both. The builder rejects modified, untracked, and ignored files in the pinned source checkout. Its `--check` mode regenerates every installed package in a temporary directory and compares complete file-path and SHA256 sets with the distributed packages, including NOTICE files.

`validate.py --project .` checks structure and the package's own inventory, but does not independently establish source provenance. It checks the package manifests, Codex skill wrappers, excluded Claude configuration files, exact package and skill counts, and `.agents/plugins/marketplace.json`. It reports unresolved links in preserved upstream Markdown separately as warnings. Use `build.py --check` with the pinned clean source checkout for the source comparison.

To run the synthetic and offline security tests:

```bash
uv run --offline --python 3.11 --with pytest python -m pytest -q tests
uv run --no-project --python 3.11 python tools/build.py --source /path/to/knowledge-work-plugins --output plugins --check
uv run --no-project --python 3.11 python tools/validate.py --project .
```

The download helper accepts only canonical HTTPS URLs under ENA's FASTQ host, checks every redirect, stages data in the destination directory, and writes a URL, byte-count, and SHA256 completion marker. It re-downloads files without a valid marker. The marker detects incomplete or changed local files; it does not authenticate the ENA server's biological data.
