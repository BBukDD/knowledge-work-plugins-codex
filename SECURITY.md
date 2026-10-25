# Security policy

This repository adapts workflows from a pinned upstream commit into Codex plugins. Reports about the adapter, its generated packages, build tools, and bundled optional scripts are welcome. Identify the affected version or commit and include a minimal reproduction when possible. The current `main` branch and latest tagged release are the relevant versions for triage; older releases may not receive fixes.

## Report a vulnerability privately

Use GitHub's **Security → Report a vulnerability** option for this repository if it is available. This opens a private security advisory visible to the maintainers. If private reporting is unavailable, open an issue that **only requests a private reporting channel**, without exploit details or sensitive data; the maintainer can then provide one. Please do not post a proof of concept, credentials, or personal data in a public issue or pull request.

If the issue is solely in the original Anthropic project, report it to that project's maintainers as well. This adapter does not supply MCP servers or SaaS credentials. An external service's security policy governs vulnerabilities in that service.

Package `NOTICE.md` hashes and source comparison help identify accidental changes, but are not signatures and do not replace normal review. The optional Python scripts have their own runtime and dependency risks; use them only after inspecting their source and required inputs.
