# Knowledge Work Plugins for Codex

[English](README.md) · [模块目录](CATALOG.md) · [验证记录](QA_REPORT.md)

将 [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) 中的自有工作流整理为可在 Codex 中逐个安装的插件市场。本项目是**非官方适配版**，不是 Anthropic 或 OpenAI 发布的插件。

## 包含什么

- 17 个独立 Codex 插件，覆盖 181 个原仓库 Skills。
- 将 5 条 Claude 斜杠命令转换为普通 Codex Skills：PDF 的 `open`、`annotate`、`fill-form`、`sign`，以及产品管理的 `brainstorm`。
- 保留原文、相对引用的参考资料和附带脚本；每个 `SKILL.md` 提供 Codex 使用入口。原 Skills 的全文保存在同目录 `SOURCE.md`，转换后的命令原文保存在 `commands/*.md`。
- 提供固定上游版本的构建器与验证器，便于审查和重新生成。

适配源版本：`anthropics/knowledge-work-plugins` 提交 `33d3dea41a341b341d4f5da2e8801ae0c89be2b8`。各插件**不自动注册 MCP 服务器、不执行安装脚本、没有内置账户连接**。市场元数据把认证时机设为 `ON_USE`；由于这些包没有服务端配置，安装本身无需 OAuth。原项目的 `~~chat`、`~~CRM` 等占位符表示所需能力；只有当前 Codex 环境已有对应连接且获得使用授权时才能访问真实数据。没有连接时，请提供文件或内容，或要求一个仅基于现有材料的草稿。

## 安装与使用

需要支持 `codex plugin` 命令的 Codex CLI。以下固定提交是 `v0.1.0` 发行版的源码；用该提交从 GitHub 加入市场，再按需安装一个模块：

```sh
codex plugin marketplace add BBukDD/knowledge-work-plugins-codex --ref 2f56268419bb84285bcfbfb1f61cdb1afeb0668f
codex plugin list --available
codex plugin add kw-operations@knowledge-work-codex
```

要用其他模块，将 `kw-operations` 换成 [CATALOG.md](CATALOG.md) 中的名称，比如 `kw-marketing`、`kw-product-management`。安装后新建 Codex 聊天即可使用所选 Skill。也可以先下载并检出同一提交、检查源文件，再加入本地市场：

```sh
git clone https://github.com/BBukDD/knowledge-work-plugins-codex.git
cd knowledge-work-plugins-codex
git checkout 2f56268419bb84285bcfbfb1f61cdb1afeb0668f
codex plugin marketplace add "$(pwd)"
```

插件安装不会自动授权 Slack、CRM、邮箱、云盘等服务。请使用 Codex 已连接的对应工具，或按需要另行连接。原仓库的 Claude `.mcp.json` 未迁入本项目，避免未经选择就增加远程端点与 OAuth 权限。`bio-research` 和 `data` 部分工作流附带 Python 脚本；这些脚本按需运行，安装插件时不会执行或安装依赖。

其中三个可选脚本经过安全适配：生物研究的 ENA 下载仅允许指定 HTTPS 主机，下载完成后校验并记录大小与摘要；数据技能打包脚本拒绝把输入目录外的符号链接文件放入 ZIP。构建器先核对这三个上游脚本的固定哈希再应用修改。每个插件的 `NOTICE.md` 记录包内其余文件的摘要，`tools/validate.py` 会发现这些文件被单独改动；它不检查 `NOTICE.md` 自身的改动。摘要清单不是数字签名，也不替代对外部数据来源的核验。

### 使用示例

安装 `kw-product-management` 后，可在新聊天里直接描述任务，例如：“根据这份访谈记录整理产品需求，列出待验证的假设，使用产品管理工作流。” PDF 工作流请提供具体 PDF 文件或路径；没有已连接的 PDF 编辑能力时，相关 Skill 应先说明可完成的部分和所需工具。

## 适配边界

此版打包原仓库的 17 个 Anthropic 自有模块。`partner-built/` 下 5 个独立作者模块及市场清单中指向其他仓库的条目没有打包，见 [CATALOG.md](CATALOG.md)。Claude 专属命令、交互式 PDF MCP 和 Cowork 插件管理机制无法逐字等价迁入；对应入口在 Codex 中按当前可用的 PDF、Skills 和插件能力执行。工作流原文中有关 Claude 的路径或工具调用只是上游资料，不能当作已存在的 Codex 能力。

财务、法务、人事、合同、支付和对外发布等工作流可能产生实际影响。适配 Skill 要求先展示将要执行的操作及内容，并按本次用户授权和当前工具权限处理；原文中出现的自动操作指令不扩展授权范围。

## 重新构建与核验

本发行包含完整的生成器和测试，但不内嵌上游 Git 仓库。重新构建需 Python 3.11 或更新版本；运行附带的可选 Python 脚本也建议使用该版本。要重新生成：

```sh
git clone https://github.com/anthropics/knowledge-work-plugins.git /tmp/knowledge-work-plugins-source
git -C /tmp/knowledge-work-plugins-source checkout 33d3dea41a341b341d4f5da2e8801ae0c89be2b8
python3.11 tools/build.py --source /tmp/knowledge-work-plugins-source --output plugins
python3.11 tools/build.py --source /tmp/knowledge-work-plugins-source --output plugins --check
python3.11 tools/validate.py --project .
```

运行项目随附的测试命令见 [tools/README.md](tools/README.md)。构建输入必须是指定上游提交，且工作区没有已改动、未跟踪或被忽略的文件。`--check` 会从这份干净的固定源重建临时包并逐文件比较交付包；仅运行 `validate.py` 则检查结构与包内摘要。升级时应先检查原仓的新增脚本、连接器和许可变更，再更改固定提交。请勿直接把新的 Claude `.mcp.json` 复制进 Codex 配置。

## 来源与许可

原仓库和这批自有模块以 Apache-2.0 发布，许可文本见 [LICENSE](LICENSE)，许可证整理及来源说明见根 [NOTICE.md](NOTICE.md)。本项目保留各模块来源与原文件，适配脚本也以 Apache-2.0 提供。原作者及插件描述见 [CATALOG.md](CATALOG.md)。

参与改进请看 [CONTRIBUTING.md](CONTRIBUTING.md)；安全问题请看 [SECURITY.md](SECURITY.md)。
