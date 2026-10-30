# Matchall for WorkBuddy

WorkBuddy 连接器适配准备包，源码版本 `0.1.0`。首测目标为 Windows WorkBuddy 5.9.3。
**自定义 MCP 已完成 OAuth 及部分真实业务验收，最终连接器身份和完整验收仍待完成；未提交、批准或发布到连接器市场。**
最低配置版本 `4.24.0` 来自所用字段的文档要求，不代表低版本已实测。

## 构建与产物

在仓库根目录使用 Python 3.12+，先安装已有 `requirements-dev.txt`：

```sh
python -m unittest discover -s tests -v
python scripts/validate.py --platform workbuddy
python scripts/package.py --platform workbuddy
```

生成 `dist/matchall-workbuddy/` 和 `dist/matchall-workbuddy-0.1.0-preparation.zip`。
ZIP 只有一层插件根目录，包含 `connector-meta.json`、`mcp.json`、根 `icon.png`、
生成的 `skills/match-service/SKILL.md`、许可证及平台资料。本源码目录不是安装目录。
业务正文与素材只在打包时从 `shared/` 读取；本平台只维护展示元数据。
`docs/skill-integrity.json` 是生成的完整性记录，不是数字签名或官方认证。
校验和打包完全离线，不会安装、登录、部署或提交商店。

Windows 建议在本仓库本地 Git 配置保持 `core.autocrlf=false`，以保留固定 schema 和
历史迁移记录的原始字节。不要修改历史哈希来消除换行问题。
原有符号链接安全测试需要相应系统权限；在具备权限的 Linux 环境完整执行，
并另测 Windows 实际检出的生成行为，不能跳过后声称全部通过。

## 本地开发连接与 Skill

1. 在 WorkBuddy「连接器 → 自定义连接器」入口使用生成包的 `mcp.json`，由本人
   通过宿主界面完成 OAuth；不要手工填入固定认证头或复用其他连接器的凭证。
2. 发现实际工具，按真实 schema 调用 `get_profile` 核对当前身份，不写死工具数量。
   MCP 连接成功不代表 Skill 已加载。
3. 如本地界面需要单独技能包，从生成目录的 `skills/match-service/` 临时压缩成
   根目录为 `match-service/` 的 ZIP，通过「添加技能 → 上传技能」导入。
   临时包不作为公共打包命令的第二个正式输出；不要另写业务正文代替生成内容。
   若有同名现有技能，先核对版本，不盲目覆盖。
4. 验证展示字段解析和实际授权行为：先私密草稿、展示实际内容，批准后再启动；
   公开需要另行批准当前预览，联系方式交换需要双方同意。
   首次写入前说明业务文本由 Matchall 及配置的模型提供方处理。

## 最终连接器 OAuth 与身份绑定

`source` 为 `matchall-workbuddy`，MCP 地址保持 `https://matchall.net/amatch/v2`，
传输字段为 `streamableHttp`。按官方文档，私有协议回调预期为：

```text
workbuddy://workbuddy/mcp/connector%3Amatchall-workbuddy/oauth/callback
```

必须以实际加载的最终连接器核对 source、issuer、scope、resource 和精确回调。
发生回环回退时记录实际 `http://127.0.0.1:{port}/oauth/callback`，未执行的路径
不标记通过。最终连接器需重新授权、工具发现、`get_profile`、重启和失效重连验证。
自定义 MCP 内部身份可能不同，改显示名称不等于加载了最终 source。
开发连接成功不能替代最终连接器 OAuth 绑定验收。

若宿主没有已核实的本地最终连接器加载入口，该项保持待验收。
不得绕过认证、改 issuer、扩大权限或代替另一身份同意。网络失败不等于服务故障。

## 验收与证据

2026-10-30 自定义 MCP 已完成 OAuth、账号核对、草稿审批、激活及一条实际匹配查询，
最终读回原意向为 `paused`、私密、版本 1，没有重复创建或重放已生效写入。
状态为 `PARTIAL_TARGET_HOST`；最终连接器加载与 source 绑定仍待验收。
详见 [本轮验收尝试记录](docs/HOST-VALIDATION-20261030.md) 的最新阶段。
Skill 文件落地、离线通过和普通 MCP 配置入口均不能替代最终连接器验收。

使用 `docs/review-cases.json` 的五正三反用例，以及 `docs/host-cases.json` 的
WorkBuddy 检查。使用授权账号与合成数据，默认私密，结束后暂停本轮意向并按实际
状态清理联系交换。单账号不能证明双方授权或跨账号隔离。

初始状态为 `NOT_RUN_IN_TARGET_HOST`。实际执行部分用例且有报告后，才记录
`PARTIAL_TARGET_HOST`；报告路径相对于 `docs/`，同步 readiness 与 host-cases 状态。
最终连接器 OAuth、Skill 或双账号用例未完成，不记录 `PASSED_TARGET_HOST`。
包校验、宿主验收、提交与批准分别记录。报告包含日期、源码身份、受测包哈希、
客户端版本、连接类型、脱敏观察和未完成项；最终交付 ZIP 哈希来自构建输出，
不能把其自身哈希循环写入包内。不得保存令牌、验证码、授权码、完整授权 URL 或真实私密联系信息。

## 审核与发布准备

- [整体状态](docs/readiness.json)、[业务用例](docs/review-cases.json)、[宿主用例](docs/host-cases.json)：各类状态的维护入口。
- [审核指南](docs/REVIEWER-GUIDE.md)：安装边界、原意向恢复、授权与账号交接。
- [提交清单](docs/SUBMISSION-CHECKLIST.md)：官方要求复核、政策适用性与发布待办。

准备材料不代表正式连接器验收或市场通过。实际调用可能晚于历史章节，
以验收报告最新阶段和对应状态文件为准。源码改动、准备包、宿主通过、市场提交及批准分别记录。

本轮回归：Linux / Python 3.12 / jsonschema 4.26.0 全量 33 项通过，校验与打包通过；
Windows 全量 33 项中 31 项通过，2 项原有符号链接测试因 WinError 1314 无法创建链接。
同环境 ChatGPT、Grok Bot 产物与基线字节一致。历史快照与完整观察保留在验收报告中。

P1/P2/P5 仅在自定义 MCP 通过；N1–N3 仅对话检查通过。正式 source、Skill 全字段解析、
完整进程重启、到期重连、受控幂等重放与冲突、双账号同意及隔离、公开测试仍待验证。
已有匹配返回 verified，但为 generic 层级并带 generic_match 警告，地区、数量、价格仍列未知，
不能据此保证实物品质或交易成功。连接曾超时，稳定性根因尚未定位。

## 输出失败的保证边界

与已有平台共用流程一致：配置校验、暂存生成、ZIP 创建及完整性检查发生在输出替换前，
这些阶段失败不会替换旧目录和旧 ZIP。
**最终写入不具备事务保证：** 共用实现先删除旧目录，再复制新目录和 ZIP。
最终目录替换、复制或 ZIP 覆盖失败可能留下缺失或不完整产物；断电、进程终止、
磁盘故障也不保证自动恢复。命令报错不得声称成功或使用残缺包，应排除写入问题后重新构建校验。
本次不新增独立回滚机制；所有故障注入只在临时测试目录执行。

## 参考

- [WorkBuddy 连接器规范](https://open.workbuddy.cn/docs/connector)
- [WorkBuddy Skill 规范](https://open.workbuddy.cn/docs/skill)
- [上游平台接入指引](https://github.com/AgentConnect/matchall-plugins/blob/main/docs/PLATFORM-INTEGRATION.md)

MIT 许可和贡献者署名沿用仓库，不代表 WorkBuddy 官方认证或发布者审核。
