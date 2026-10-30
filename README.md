# Matchall Plugins

Matchall 的多平台插件源码仓库。ChatGPT、Grok Bot 和 WorkBuddy 共用技能与品牌素材，
保留各自的清单、MCP 配置、版本和审核记录。匹配服务后端继续由独立的
`match-service` 仓库维护。

| 平台 | 插件标识 | 当前源码版本 | 生成后的清单 |
| --- | --- | --- | --- |
| ChatGPT | `matchall-chatgpt` | `0.1.10` | `plugin.json` |
| Grok Bot / Cursor 格式 | `matchall-grok-bot` | `0.1.2` | `.cursor-plugin/plugin.json` |
| WorkBuddy | `matchall-workbuddy` | `0.1.0` | `connector-meta.json` |

这些版本标识准备包；本次仓库合并不发布版本、不提交商店审核，也不更新已安装插件。
历史宿主验收结果保存在各平台的 `docs/` 中，不代表合并后新包已经完成宿主验收。

## 开发与打包

需要 Python 3.12 或更新版本。从仓库根目录运行：

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate.py
python scripts/package.py
```

也可以指定单个平台：

```sh
python scripts/validate.py --platform chatgpt
python scripts/package.py --platform grok-bot
```

输出包括自包含目录 `dist/matchall-chatgpt/`、`dist/matchall-grok-bot/`、`dist/matchall-workbuddy/`，
以及对应的 `*-preparation.zip`。每个 ZIP 只包含一个插件，技能和素材均为真实文件，
没有跨目录依赖或符号链接。脚本校验 ZIP 内容并输出 SHA-256；相同源码生成相同 ZIP。
生成目录会在重新构建时刷新，请修改源文件，不要修改 `dist/`。

**仓库根目录和 `platforms/<平台>/` 都不是可直接安装的插件目录。**
安装或上传时使用生成目录/ZIP，并遵循目标宿主的实际安装流程。
只接受 Git 仓库根目录的平台，需要先核实其子目录能力或另行设计经授权的分发方式，
不能直接把本仓库 URL 当作已兼容的安装入口。

## 源码布局

```text
shared/
  skills/match-service/SKILL.md   # 唯一的业务操作与授权规则
  assets/                        # 共用图标和 Logo
platforms/
  chatgpt/                       # 清单、MCP 配置、平台说明及审核资料
  grok-bot/
  workbuddy/                     # 原生连接器准备包；自定义 MCP 部分验收，正式身份待核实
platforms.json                   # 平台标识、插件名称和打包格式
schemas/                        # 固定版本的 Agent Plugins 校验规则
scripts/                        # 共用校验与本地打包
tests/                          # 打包隔离、迁移完整性与失败路径回归
docs/                           # 接入指引与迁移说明
```

修改业务流程时编辑 `shared/skills/match-service/SKILL.md`；修改平台展示、
审核材料或连接格式时编辑对应 `platforms/` 目录。平台名称和版本独立管理。
CI 运行离线校验、回归测试和本地打包，没有发布或部署步骤。

## 文档

- [其他平台接入指引](docs/PLATFORM-INTEGRATION.md)：MCP 直连、插件适配、授权约束和验收。
- [迁移记录](docs/MIGRATION.md)：基线、Git 历史、原仓库与未提交资料的保留方式。
- [ChatGPT 说明](platforms/chatgpt/README.md)与[审核状态](platforms/chatgpt/docs/READINESS.md)。
- [Grok Bot 说明](platforms/grok-bot/README.md)与[历史验收](platforms/grok-bot/docs/host-validation-2026-10-19.md)。

服务地址为 `https://matchall.net/amatch/v2`。用户在宿主 OAuth 界面授权；
不要把访问令牌、验证码、私钥或真实联系方式写进仓库、配置样例或验收记录。
草稿审核、启动匹配、公开摘要和联系方式交换是不同的授权步骤。

插件源码采用 [MIT](LICENSE) 许可；不代表后端服务或第三方平台的许可与审核状态。
