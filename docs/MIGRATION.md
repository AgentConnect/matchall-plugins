# 双仓库合并记录

2026-10-29。目标源码仓库：`AgentConnect/matchall-plugins`。

## 基线与保留范围

迁移前分别 fetch 远程，并确认本地 HEAD 的文件树与各自 `origin/main` 相同。
导入基线为：

| 原仓库 | 远程 main |
| --- | --- |
| `AgentConnect/matchall-chatgpt` | `85aca38` |
| `AgentConnect/matchall-grok-bot` | `526e269` |

ChatGPT 工作目录另外包含尚未提交的 0.1.10 审核准备资料。已将所有受版本控制
及非忽略的本地源码文件复制到新仓库，并以 `354f5c5` 独立保存；没有覆盖或清理原工作目录。
原仓库中的虚拟环境、缓存、构建产物及忽略的敏感文件未导入。

新仓库保留 ChatGPT 的原始提交链，并通过合并提交保留 Grok Bot 的完整 main 历史。
Grok 文件先完整导入独立子目录，再进行共用内容抽取，因此同名文件不会相互覆盖。
[来源清单](source-inventory.json)记录导入时文件的 SHA-256 和完整远程提交号。

## 路径迁移

| 原位置 | 新源码位置 |
| --- | --- |
| 两边 `skills/`、`assets/` | `shared/skills/`、`shared/assets/`，原内容完全相同 |
| ChatGPT `plugin.json`、`mcp.json`、`docs/` | `platforms/chatgpt/` 下原相对路径 |
| Grok `.cursor-plugin/`、`mcp.json`、`docs/` | `platforms/grok-bot/` 下原相对路径 |
| ChatGPT `schemas/` | 根目录 `schemas/` |
| 两边校验、打包与 CI | 根目录 `scripts/` 与 `.github/workflows/validate.yml` |

平台清单仅更新 `repository` 为新仓库地址；插件名称、版本、MCP 配置、
业务技能、ChatGPT 展示/审核元数据、Grok 历史验收资料均保留。
平台 README 增加新构建路径。日期明确的审核资料及其中旧仓库链接保留为历史证据，
不批量替换它们以免把过去的验证结果错误归属到新仓库。

新包保留各平台 README、LICENSE、MCP、清单、素材、技能和审核文档。
便于离线校验的 Agent Plugins schema 随 portable 包保留。
开发用 Python 脚本和依赖文件集中在源码仓库，不再重复放进每个运行时包。

## 切换和后续验收

从本仓库继续维护源码。原两个远程仓库暂时保留，未删除、归档或改名。
现有宿主连接、商店草稿、OAuth 设置和后端服务不因源码合并而改变。
新生成包需要单独完成目标宿主验收；过去的 Grok 开发连接验收和 ChatGPT 开发排练
不能代替新包验收。发布、商店提交、安装或旧仓库归档各自需要对应授权。

尤其注意：本仓库是源码 monorepo。原 Grok 提交材料中“提交仓库根目录”的步骤仅适用
旧仓库，不能照抄到新根目录。若平台接受 MCP URL，可在经授权的提交中使用既有服务地址；
若要求完整插件，按平台支持的方式提供 `dist/matchall-grok-bot/`。
若仅接受 Git 根目录且不支持子目录，先解决其分发入口，不能声称已经完成安装切换。
