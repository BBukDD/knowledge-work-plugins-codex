# 模块目录与范围

本目录以 Anthropic 上游提交 `33d3dea41a341b341d4f5da2e8801ae0c89be2b8` 为准。表中的 Skills 数量来自该提交的 `skills/*/SKILL.md`；“新增入口”指 Claude command 转换出的 Codex Skill。每行均可单独安装，无需安装整套市场。

| Codex 插件 | 工作领域 | 原 Skills | 新增入口 |
| --- | --- | ---: | ---: |
| `kw-bio-research` | 生物研究 | 6 | 0 |
| `kw-cowork-plugin-management` | 插件与技能管理，按 Codex 能力改写入口 | 2 | 0 |
| `kw-customer-support` | 客服 | 5 | 0 |
| `kw-data` | 数据分析 | 10 | 0 |
| `kw-design` | 设计 | 7 | 0 |
| `kw-engineering` | 工程 | 10 | 0 |
| `kw-enterprise-search` | 企业资料检索 | 5 | 0 |
| `kw-finance` | 财务 | 8 | 0 |
| `kw-human-resources` | 人事 | 9 | 0 |
| `kw-legal` | 法务 | 9 | 0 |
| `kw-marketing` | 市场营销 | 8 | 0 |
| `kw-operations` | 运营 | 9 | 0 |
| `kw-pdf-viewer` | PDF 阅读与处理 | 1 | 4 |
| `kw-product-management` | 产品管理 | 8 | 1 |
| `kw-productivity` | 个人效率 | 4 | 0 |
| `kw-sales` | 销售 | 36 | 0 |
| `kw-small-business` | 小型企业流程 | 44 | 0 |
| **合计** | | **181** | **5** |

新增入口的 Skill 名称为 `kw-pdf-viewer` 中的 `command-open`、`command-annotate`、`command-fill-form`、`command-sign`，以及 `kw-product-management` 中的 `command-brainstorm`。在 Codex 中直接描述任务并指明相应 Skill；原 Claude `/command` 语法不是安装入口。

## 未打包条目

`partner-built/` 下的 `slack-by-salesforce`、`apollo`、`common-room`、`brand-voice`、`zoom-plugin` 由不同作者提供，含 44 个顶层 Skills、Zoom 模块中 27 个嵌套 Skills，合计 71 个，另有 10 条 commands。它们有自己的许可、连接器和更新路径，未并入本版包。上游市场清单中指向其他 Git 仓库的条目也没有抓取或自动安装；原始清单作为资料保存在 [UPSTREAM_MARKETPLACE.json](UPSTREAM_MARKETPLACE.json)。需要时可针对单项来源、许可及连接权限再做迁移。

## 功能差异

| 上游概念 | 本项目的处理 |
| --- | --- |
| `SKILL.md` 与参考资料 | 独立 Codex Skill 入口；原文存为 `SOURCE.md`，参考资料与相对路径保留 |
| `commands/*.md` | 转成自然语言触发的 Skill，不依赖 Claude `/command` 和 `$ARGUMENTS` |
| `~~connector` 占位符 | 在入口说明中映射为当前已连接工具所提供的能力；缺少连接时使用用户材料或说明限制 |
| `.mcp.json` 与 OAuth | 不自动迁入；由用户在 Codex 中独立选择和连接服务 |
| Python 附带脚本 | 保留并按需运行；三个下载/打包脚本有哈希锁定的安全适配，见各包 `NOTICE.md`；安装期间不执行 |
| PDF 专属 `display_pdf`、`viewUUID` | 使用当前 Codex 可用的 PDF 能力；原有实时标注语义无法保证完全一致 |
| Cowork 插件配置与路径 | 使用 Codex Skills/插件路径和工具；上游机制只供参考 |

源仓：[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)。本项目不是官方发行版。
