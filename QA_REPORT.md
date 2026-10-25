# 验证记录

验证日期：2026-10-25。上游基线：`33d3dea41a341b341d4f5da2e8801ae0c89be2b8`。本机 Codex CLI：`0.164.0-alpha.11.1`。

## 构建与静态校验

| 检查 | 结果 |
| --- | --- |
| 从干净、固定版本的上游重新生成并比较交付包 | 17 个插件、181 个原 Skill、5 个命令 Skill；逐文件比较通过 |
| `tools/validate.py --project .` | 17 个插件、186 个 Skill，0 条上游链接警告 |
| Codex Skill Creator `quick_validate.py` | 186/186 个 Skill 有效 |
| Python 3.11 离线测试 | 32/32 通过 |
| Ruff，basedpyright（适配器工具与测试） | 通过；0 个类型错误 |
| 重建一致性 | 连续构建前后 734 个插件包文件的哈希均相同 |

`--check` 会拒绝上游源码被修改、未跟踪或被 Git 忽略的文件；也会发现即使同时改动 `SOURCE.md` 和包内 `NOTICE.md` 摘要清单的情况。单独的 `validate.py` 用于结构和包内摘要检查，不能独立证明来源真实性。

## Codex 实际使用

- 使用独立的 `CODEX_HOME` 运行 `codex plugin marketplace add`：识别市场 `knowledge-work-codex`。
- `codex plugin list --available --json` 返回 17 个可选插件。
- `codex plugin add kw-operations@knowledge-work-codex --json` 成功；安装缓存包含 9 个 `SKILL.md` 和 9 个 `SOURCE.md`，没有 MCP 配置。
- 最终 ZIP 的 SHA256 记录在同名 `.sha256` 文件。从 ZIP 解压后，独立配置仍能列出 17 个插件并安装 `kw-product-management`；安装副本包含 8 个原 Skill 和 `command-brainstorm`，没有 MCP 配置。解压副本的完整校验通过。
- 在新的 Codex CLI 会话里，`kw-operations/process-doc` 读取入口与上游原文，只用给定的虚构事件交接事实生成 SOP，并标出未说明的角色和时间规则。
- `kw-enterprise-search/search` 在没有 Slack、邮件材料和服务连接的测试里没有编造决定，明确要求提供消息与时间信息。
- `kw-cowork-plugin-management/create-cowork-plugin` 为 Codex 给出根目录 `plugin.json` 与 `skills/meeting-summary/SKILL.md` 结构，没有输出 Claude 专用包结构。

## 安全与功能边界

离线测试覆盖 ENA HTTPS 主机和跳转限制、下载中断与长度不符、缓存摘要校验、临时文件清理，以及 ZIP 对外部符号链接与目录内输出的拒绝。安全修补只作用于生成包中的三个可选脚本；181 份 `SOURCE.md` 与固定上游版本逐字一致。

上游根 `LICENSE` 的标准 Apache-2.0 文本后附有无关草稿；本项目根许可文件及 5 个继承根许可的插件包使用同一份干净的标准文本。其余 12 个插件保留各自的上游许可文件，来源与修改见根 [NOTICE.md](NOTICE.md) 及各包 `NOTICE.md`。

原 Claude MCP/OAuth 连接、实时 PDF viewer、合作方插件及外部 Git 市场条目没有自动迁入。Skill 的实际外部服务能力取决于当前 Codex 已连接且已获授权的工具；本轮没有连接真实 SaaS，也没有执行上游科研脚本或真实 ENA 下载。`NOTICE.md` 的包内摘要不是数字签名。
