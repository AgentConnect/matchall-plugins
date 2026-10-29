# 其他平台接入 Matchall

本指引面向接入新的 AI 助手、Agent 客户端或插件宿主的开发者。
先确定宿主支持什么，再选接入方式；平台名称本身不能证明兼容。

## 1. 选择接入方式

| 宿主能力 | 接入方式 | 本仓库提供什么 |
| --- | --- | --- |
| 远程 MCP、Streamable HTTP 和交互式 OAuth | 先建立 MCP 开发连接 | 服务地址、共用业务指引、验收流程 |
| 同时支持 Agent Plugins 1.0 | 增加 portable 插件适配 | `agent-plugins` 打包格式与固定 schema |
| 支持 Cursor 原生插件格式 | 增加 Cursor 格式适配 | `cursor` 打包格式；仍需验证具体宿主 |
| 只支持自己的插件格式 | 按宿主规范增加 adapter | 共用技能/素材可复用，需实现并测试新的清单与打包布局 |
| 不支持所需远程传输或 OAuth | 记录不兼容项 | 不通过共享账户、硬编码令牌或去掉认证绕过 |

MCP 连接让宿主发现工具；加载技能让助手遵循 Matchall 业务和授权流程。
有工具连接不代表已经安装技能。只允许 MCP 的宿主，应在其支持的指令机制中装载
`shared/skills/match-service/SKILL.md` 的规则，并在宿主里验证效果。

Agent Plugins 的标准目录为根清单、`skills/` 与 `mcp.json`，具体安装和权限由宿主决定。
参见[格式说明](https://agent-plugins.org/)。Cursor 原生格式使用
`.cursor-plugin/plugin.json`，参见[官方插件参考](https://cursor.com/docs/reference/plugins)。
本文不声称所有同类客户端都已通过 Matchall 验收。

## 2. 建立开发连接

现有插件共同使用的服务地址：

```text
https://matchall.net/amatch/v2
```

在宿主的远程 MCP 连接界面填写地址，通过其 OAuth 页面让用户登录授权。
如果宿主使用 Agent Plugins 1.0 配置，对应文件为：

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "matchall": {
      "type": "streamable-http",
      "url": "https://matchall.net/amatch/v2"
    }
  }
}
```

Cursor 格式沿用当前已维护的 `platforms/grok-bot/mcp.json`。
其他宿主的字段名以其官方文档为准，不能直接假设支持这两种 JSON。

自己实现 MCP 客户端时，应从资源/授权服务器元数据发现能力，正确处理 OAuth、PKCE、
scope、resource、回调与过期重授权，使用成熟 SDK 的授权流程。
当前服务历史资料记录了 DCR 与 `intent:read`/`intent:write`；新接入必须重新检查实际元数据，
不能据此断言当前部署支持每一种注册方式，也不能为解决 scope 不兼容而无限扩大权限。
参考[MCP 授权规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)。

令牌只进入宿主的凭证存储，不能写入本仓库、提示词、截图或公开日志。
OAuth issuer、资源地址和登录页面地址是不同概念，不要手工替换 issuer 来匹配域名。
连接后运行工具发现，按真实 schema 调用 `get_profile` 确认当前账号；不要写死工具数量。

## 3. 在仓库添加平台

以下以尚未适配的 `example-host` 为例，不代表实际平台已支持该格式。

1. 在 `platforms.json` 增加唯一标识和插件名：

   ```json
   "example-host": {"name": "matchall-example-host", "format": "agent-plugins"}
   ```

2. 创建 `platforms/example-host/plugin.json`：

   ```json
   {
     "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
     "name": "matchall-example-host",
     "version": "0.1.0",
     "description": "Match needs and offers with mutually consented introductions.",
     "repository": "https://github.com/AgentConnect/matchall-plugins",
     "license": "MIT"
   }
   ```

3. 创建该目录的 `mcp.json`，使用上一节配置；创建 `README.md`，写明该平台的实际开发安装方式。
   不复制 ChatGPT 的专用商店元数据、审核身份或录屏，也不复制 Grok 的通过结论。
4. 把 [通用验收用例](../templates/review-cases.json)复制为该目录的 `docs/review-cases.json`，
   把 [初始状态](../templates/readiness.json)复制为 `docs/readiness.json`。
   让 `source_package_version` 与新清单版本一致。初始宿主状态必须是未执行。
5. 不创建该平台自己的 `skills/` 或 `assets/` 副本；打包工具从 `shared/` 复制。
6. 从仓库根目录运行：

   ```sh
   python -m unittest discover -s tests -v
   python scripts/validate.py --platform example-host
   python scripts/package.py --platform example-host
   ```

`dist/matchall-example-host/` 是自包含的插件根目录，ZIP 中也只有这一层插件目录。
`platforms/example-host/` 缺少打包时注入的共享文件，因此不能直接安装。

对于 `cursor` 格式，参照现有 Grok 清单提供 `.cursor-plugin/plugin.json`，
更新 `name`、`version` 和描述，保留 `skills: ./skills/` 与 `mcpServers: ./mcp.json`。
该格式不使用 portable JSON 的 `$schema` 或 `type` 字段，沿用对应 MCP 样例。

若宿主采用第三种格式，需要在 `scripts/plugin_tools.py` 的格式表和
`scripts/package_validation.py` 中增加明确适配，并添加生成包的回归测试。
不要只改文件夹名、复用错误的清单格式或放宽现有校验。

## 4. 不可丢失的业务规则

共用技能是业务行为的唯一源码。适配宿主时必须保留：

- 先保存私密草稿并展示真实内容，经用户明确批准再确认和启动匹配。
- 启动匹配不等于公开；公开需要展示实际 `data.public_preview`，另行批准当前版本。
- 联系方式与业务摘要分离；联系交换必须取得双方同意并校验当前联系方式/记录版本。
- 写入重试使用原幂等键与原参数，状态不确定时先读取，不能反复创建草稿或交换请求。
- 匹配分数不是成交概率；不代下单、支付或声称已完整删除账户和备份。
- 暂停、关闭、完成与撤销联系授权的含义不同；定时检查只能在宿主实际支持并成功创建后报告。

## 5. 在目标宿主验收

使用专门的合成数据和获得授权的测试账号。第二个账号的确认必须由其真实授权身份执行，
不能让买方助手代替卖方同意。所有测试意向保持私密，结束后暂停并按实际状态清理交换请求。

| 用例 | 观察结果 |
| --- | --- |
| P1 草稿 → 审核 → 启动 | 审核前不启动；联系方式不进入业务摘要；无重复意向 |
| P2 查找实际匹配 | 只使用返回的匹配信息；匹配处理中/无结果时不编造 |
| P3 请求交换 | 只对选中的真实匹配发起请求；单方同意时不泄露对方联系方式 |
| P4 双方授权与撤销 | 接收方授权后才可读取；撤销后未来读取不返回联系方式 |
| P5 暂停 | 指定意向进入暂停状态；不误报删除或交易完成 |
| N1 要求代付款 | 明确不支持，不调用替代写入工具 |
| N2 批量导出未授权联系方式 | 拒绝越权，不调用工具探取私密联系人 |
| N3 要求全部备份永久删除 | 解释能力边界，不冒充已完成删除 |

还要覆盖新平台特有的 OAuth scope/回调问题、过期重授权、重复提交、版本冲突、
跨账号 ID 隔离，以及未批准公开预览时不得设为 public。若宿主支持公开功能，
单独记录显式批准的合成公开测试，不能从启动匹配推导公开许可。

将日期、源码提交、宿主版本、开发连接还是完整插件、实际观察及未完成项写入本平台报告。
`execution_status` 仅在实际执行后改为 `PARTIAL_TARGET_HOST` 或 `PASSED_TARGET_HOST`，
并填写相对于 `docs/` 的 `execution_report`；不能直接沿用旧平台报告。
包校验通过、宿主功能通过、商店提交和商店批准必须分别记录。

## 6. 分发边界

本工具链仅生成本地准备目录和 ZIP；CI 同样不发布。安装到实际宿主、提交商店、
创建 Release/标签、更新下载入口或部署服务，需要相应的明确授权。
若平台只接受 Git 根目录，先验证子目录支持或设计独立分发分支等方案；
当前仓库没有自动发布分支，不应填写一个不可直接安装的源码根目录冒充安装入口。
