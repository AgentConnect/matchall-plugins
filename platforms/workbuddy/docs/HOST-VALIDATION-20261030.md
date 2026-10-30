# WorkBuddy 最终连接器验收尝试记录

日期：2026-10-30（Asia/Shanghai）。本文按阶段保留观察，以下首次尝试和中间阶段的
`NOT_RUN_IN_TARGET_HOST` 为历史状态；截至文末最新阶段，自定义 MCP 的 OAuth、
真实账号查询及部分业务用例已执行，总体为 `PARTIAL_TARGET_HOST`。
最终连接器身份尚未核实；本报告不是完整宿主通过证明，也不是市场提交材料。

## 受测对象与证据边界

- 基线提交：`67841b8f8024ed4d390d26ef4be19609108d8165`。
- 分支：`Feature/workbuddy-adapter`，包含既有未提交的 WorkBuddy 适配。
- 构建前 74 个 Git 跟踪及未忽略新增文件按实际字节生成 SHA-256 清单；
  清单规范 JSON 的 SHA-256 为 `accd8bb018a5ec6f4e0f59a04e26025888950f1cd6a847ef3e5a0192fec392d4`。
  此标识对应报告与状态更新前的源码，不是 Git 提交或数字签名。
- 客户端界面实际显示 Windows WorkBuddy `5.9.3`。
- 候选包标识：本轮首次成功构建后冻结的 `candidate-before-host.zip`，
  来自 `matchall-workbuddy-0.1.0-preparation.zip`。正式连接类型尚未建立。
- ZIP 哈希及源码逐文件清单保存在包外的 `dist/acceptance-20261030/`；
  报告入包后的重建产物另行记录，不继承候选包的宿主验收结论。
- 预期 source 为 `matchall-workbuddy`，服务地址为 `https://matchall.net/amatch/v2`，
  传输字段为 `streamableHttp`；以上为包配置，尚未在最终运行连接器中核实。

## 本轮离线复验

| 环境与检查 | 实际结果 |
| --- | --- |
| Windows / Python 3.12.14 / 项目虚拟环境 | 31 项中 29 项通过，2 项符号链接测试报 WinError 1314 |
| Windows 全平台校验与打包 | ChatGPT、Grok Bot、WorkBuddy 均通过 |
| Ubuntu / Python 3.12.3 / 已有 jsonschema 4.10.3 | 同一源码快照 31 项全部通过，包含真实符号链接测试；全平台校验与打包通过 |

首次运行因默认临时目录权限报 WinError 5，改用仓库内忽略目录作为 TEMP/TMP 后正常运行。
没有修改或跳过测试，也没有更改 Windows 安全设置。Ubuntu 的既有依赖版本不同于
`requirements-dev.txt` 的 4.26.0，该结果只能作为补充验证；不能称为锁定依赖环境全量通过。
本轮未安装新依赖。日志保留在包外；本报告的结论不依赖读取机器私有路径。

## 客户端入口与 Skill 观察

1. 启动现有客户端，进入「专家·技能·连接器 → 连接器」。可见连接器市场和「自定义连接器」。
2. 「自定义连接器」打开「MCP 服务管理」；「添加 MCP」打开普通 `mcpServers` JSON
   编辑器，没有在这些入口看到最终 `connector-meta.json` 或完整准备包的导入选项。
   未修改或保存该配置。此观察不证明客户端所有入口均不支持最终包加载。
3. 官方插件文档还描述了一般插件管理能力，但没有据此确认该插件机制会加载本包的
   connector source。不得将另一种插件清单、显示名称或普通 MCP 配置当作最终身份绑定。
4. 通过「技能 → 添加技能 → 上传技能 → 选择 ZIP 文件」选择了由冻结候选包提取的
   `match-service-local.zip`，根目录为 `match-service/`，未复制或另写业务正文。
   客户端进入安全检测流程；没有点击「跳过检测，直接安装」或修改安全选项。
5. 随后只读确认本机已安装 `match-service/SKILL.md`，与候选包中的文件逐字节一致，
   SHA-256 为 `24b892d19f8648d13a8fa9d1bd0c10b8421d912fd31fd58b04452e2aa29e1904`。
   未独立取得安全检测最终结果；此文件核对不证明全部展示字段已解析或授权规则已生效。
6. 用户确认正在同时操作客户端，代理随后停止界面操作。新出现的草稿对话报告
   Matchall 连接器未连接、无法真正保存草稿，并要求补齐需求。该响应仅为辅助观察，
   未取得真实工具调用证据，不计为 P1 或 WB2 通过，也不把用户操作归因于代理。

## OAuth 元数据尝试

未携带凭证，对 MCP 地址及以下候选元数据地址执行公开 GET：

- `https://matchall.net/.well-known/oauth-protected-resource/amatch/v2`
- `https://matchall.net/.well-known/oauth-protected-resource`

默认执行环境最初返回 WinError 10013；获得网络执行权限后，这三个地址均返回 HTTP 403，
没有 `WWW-Authenticate` 头。网页读取工具也未取得元数据。
403 的具体来源未确认，不据此判定后端服务故障、OAuth 不兼容或实际元数据地址。

未取得实际 issuer、scope、resource 或 PKCE 能力；未动态注册客户端、登录、交换令牌、
发现工具或调用 `get_profile`，也未建立两个测试账号的授权身份。
预期私有协议回调仍为
`workbuddy://workbuddy/mcp/connector%3Amatchall-workbuddy/oauth/callback`，
但它只是官方格式和本包 source 推导的预期值。私有协议及回环回退均未实测。

## 逐项验收状态

| 用例 | 状态 | 观察或缺失条件 |
| --- | --- | --- |
| WB1 最终连接器与 OAuth | 未执行／阻塞 | 未核实最终包加载入口；元数据读取未成功 |
| WB2 Skill 与草稿审批 | 未执行 | 文件安装字节核对完成；展示解析和真实业务审批未测 |
| WB3 重启、到期与重连 | 未执行 | 尚未建立最终连接器授权 |
| WB4 幂等重试 | 未执行 | 未执行写入；没有注入宿主或生产故障 |
| WB5 公开审批与版本冲突 | 未执行 | 审批拦截尚未测；本轮不授权实际公开，公开冲突路径留待后续 |
| WB6 双账号同意、撤销与隔离 | 未执行 | 两个账号尚未分别完成最终连接器 OAuth |
| P1 私密草稿、审核、启动 | 未执行 | 未取得最终连接器工具调用证据 |
| P2 实际匹配 | 未执行 | 未创建本轮意向，没有实际匹配 ID |
| P3 单方交换请求 | 未执行 | 无本轮真实匹配和交换请求 |
| P4 双方同意与撤销 | 未执行 | 无分别授权身份及交换版本 |
| P5 暂停 | 未执行 | 本轮未创建可暂停意向 |
| N1 代付款 | 未执行 | 尚未在受测连接器会话中验证 |
| N2 越权联系人导出 | 未执行 | 尚未在受测连接器会话中验证 |
| N3 全部账户及备份删除 | 未执行 | 尚未在受测连接器会话中验证 |

代理未调用 Matchall 业务写入、创建测试意向、发起交换或公开内容，因此没有代理创建的
业务数据需要清理；用户独立会话的数据状态未经工具核实，不能声称已经统一清理。

## 恢复验收的顺序

1. 核实官方支持且能保留最终 source 的本地加载方式；若需要平台开发预览权限，
   先取得该权限。不通过提交市场、改身份或手写凭证绕过这一前置条件。
2. 复核网络路径并读取实际元数据；仅使用宿主支持的 OAuth。账号持有人各自完成登录。
3. 加载固定候选包，验证 source、回调、真实工具 schema 和 `get_profile` 身份，再测重启与重连。
4. 使用本轮唯一标签和两个账号的合成数据，依 P1–P5、N1–N3、WB1–WB6 继续。
   业务文本处理说明必须先于首次写入；草稿启动及每方联系授权分别确认。
   不确定写入先读状态，同一写入重试保留原幂等键和参数；版本冲突重新展示并确认。
5. 保持意向私密；无单独公开批准不得公开。结束后暂停本轮双方意向、撤销或取消交换，
   读取确认实际状态。仅在真实宿主用例执行且有证据后更新为 `PARTIAL_TARGET_HOST`。
   本轮未授权的公开路径未测，不能记录 `PASSED_TARGET_HOST`。

市场提交、批准及 submission_ready 均保持 false。未发布、部署或创建 Release。

参考：[WorkBuddy 连接器规范](https://open.workbuddy.cn/docs/connector)、
[WorkBuddy 插件说明](https://www.codebuddy.cn/docs/workbuddy/Plugins)。

## 后续阶段：自定义 MCP 与已安装 Skill

本阶段先验证开发连接业务，最终连接器身份另行验收。前面的记录保留为首次尝试历史，
以下为本阶段的新观察；不得将诊断客户端结果计为 WorkBuddy OAuth 成功。

### 公开元数据读取已恢复

403 响应明确返回 Cloudflare Error 1010 / `browser_signature_banned`。
根据 [Cloudflare 官方说明](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/)，
默认 Python 请求标识可能被拦截。使用真实的应用标识
`Matchall-WorkBuddy-Acceptance/0.1.0 (public OAuth metadata diagnostic)` 后读取成功；
没有伪装浏览器、更改网站安全策略、替换 issuer 或扩大请求权限。

| 只读探测 | 实际结果 |
| --- | --- |
| `GET https://matchall.net/.well-known/oauth-protected-resource/amatch/v2` | 200；resource 为原 MCP 地址，authorization_servers 为 `https://www.amatch.me/oauth/match`，资源 scope 为 `intent:read`、`intent:write` |
| `GET https://www.amatch.me/.well-known/oauth-authorization-server/oauth/match` | 200；issuer 与上项一致，公告 PKCE S256、公共客户端、authorization_code 和 refresh_token |
| 原 MCP 地址的匿名 `POST initialize` | 401；`WWW-Authenticate` 指向上述资源元数据，并要求 `intent:read intent:write` |

授权服务器公告的 authorize、token、register 分别位于 `https://matchall.net/oauth/match/`
下。其全局 scope 还包含 `interest:express`；本轮没有据此请求额外权限。
issuer 带路径，授权服务器发现文档是在 `/.well-known/oauth-authorization-server/oauth/match`，
不能把 well-known 路径简单追加到 issuer 后面。元数据中的能力公告不是协议全流程实测。

本次探测不携带凭证、不动态注册、不登录、不调用业务工具。
包外证据为 `dist/acceptance-20261030/oauth-discovery-resolved.json`。
这些结果解决了诊断程序的元数据读取问题，尚未证明 WorkBuddy 自身的授权请求可用。

### 开发连接已保存，等待本人信任与授权

通过 WorkBuddy 5.9.3 的「自定义连接器 → 添加 MCP」界面保存：

```json
{
  "mcpServers": {
    "matchall": {
      "type": "streamableHttp",
      "url": "https://matchall.net/amatch/v2"
    }
  }
}
```

保存前自定义 `mcpServers` 为空；保存后只读核对与源码配置相同，没有认证头。
列表仍保留原插件提供的 MCP。新增 `matchall` 显示未启用，并提示
「首次连接此 MCP 服务需要您的信任确认」，提供「信任」按钮。
代理没有点击信任按钮，已将安全确认及后续 OAuth 登录交还账号持有人。

连接类型为 `CUSTOM_MCP_WITH_INSTALLED_SKILL`；当前只是开发连接配置已落地。
尚未取得宿主工具发现、`get_profile` 或当前账号身份结果，两个独立授权身份未建立。
P1–P5、N1–N3、WB1–WB6 仍未完成；未创建本轮意向或联系交换。
总体状态继续保持 `NOT_RUN_IN_TARGET_HOST`。实际执行业务用例并取得证据后，
才能同步改为 `PARTIAL_TARGET_HOST`，且仍须标明最终 source 与完整包身份未验收。

恢复顺序：本人完成信任及 OAuth → 核对宿主实际工具和 `get_profile` →
确认 Skill 已加载 → 单账号草稿审批及反例 → 分别授权的双账号匹配、交换与撤销 →
暂停本批次意向并读取确认。所有意向保持私密，草稿启动和双方联系授权分别确认。

### 本人尝试后的实际阻塞：回调路径不兼容

账号持有人随后报告认证失败。只读观察到 `matchall` 已启用，但仍显示「需要认证」。
2026-10-30 11:10:39–11:10:43（Asia/Shanghai）的宿主诊断显示：资源元数据与授权服务器
元数据均返回 200；两次 `POST /oauth/match/register` 均返回 400，错误类型为
`InvalidClientMetadataError`，错误原文是
`redirect_uri is not allowed by the invitation callback policy`。
因此该次失败已定位到动态客户端注册，不能继续归因为诊断程序先前的 Cloudflare 403。
也没有证据显示该次请求已经到达 scope 审批或账号登录阶段。

只读检查 WorkBuddy 5.9.3 安装代码确认：OAuth 先尝试私有协议回调，注册被拒绝后自动
尝试本机回环；两种回调都固定使用 `/oauth/callback`。没有找到可在当前自定义 MCP 配置
中修改此回调路径的受支持字段。没有补写未经证实的配置项或修改安装程序。

通过已连接的 GitHub 读取到 OAuth 所属仓库 `AgentConnect/awiki-gateway`，固定基线为
`6b1e04313eb1d585429905505de8987c5eadda01`。其中
`crates/message-gateway/src/oauth/matching/registration.rs` 的
`is_loopback_callback` 仅接受 `/callback`。同仓 `docs/oauth/matching-invitations.md`
也明确记录该精确路径、IP 字面量和端口限制。此代码与宿主固定的 `/oauth/callback`
不兼容，符合实际错误；远端 main 的代码不等于独立确认了当前生产二进制和配置。

修复方向是在已开启 `allow_loopback_callbacks` 时，同时支持两个精确路径
`/callback` 和 `/oauth/callback`，保留 HTTP、本机 IP 字面量、1024–65535 端口、
无 userinfo/query/fragment、规范 URI 和每个已注册客户端的完整回调精确绑定。
不开放任意私有协议、任意路径、任意 localhost 端口或外部主机。
该修复属于网关，不属于本 Python 插件包；准备包配置无法修复服务端拒绝。

脱敏宿主事件保存在包外 `dist/acceptance-20261030/workbuddy-oauth-failure.json`；
网关候选源码与测试位于同目录下的隔离快照，不写入插件正式包。
当前本人信任步骤已完成，OAuth 实际失败，工具发现、身份核对和全部业务用例仍未执行。
网关修复尚未部署，现有服务、生产配置和数据库均未修改。

### 网关兼容补丁与本地验证

已在上述固定基线的包外隔离源码快照中准备两文件补丁：注册路径判定及其同意策略文档。
实现仅增加精确的 `/oauth/callback`，仍受原有回环开关及完整 URI 限制约束。
补丁文件为 `dist/acceptance-20261030/gateway-callback-fix.patch`，不进入插件 ZIP；
它不是对远端仓库、当前线上代码或生产配置的修改。

先加入两项回归测试，在未修复源码上均失败，其中注册错误与宿主实际错误一致。
应用修复后，注册模块 14 项测试全部通过：包含旧路径、新路径、IPv4/IPv6、关闭开关、
恶意主机/端口/凭证/查询/片段/编码路径拒绝，以及注册后重启仍保持完整回调集合精确绑定。
工作区格式检查和 `message-gateway` 库的 Clippy 检查（警告视为错误）通过。
反向补丁检查通过；没有修改 Cargo.lock 或引入新项目依赖。

本地工具为 Windows Rust/Cargo 1.93.1，区别于网关锁定的 1.88.0；为已有 stable 工具链
补装 rustfmt/Clippy，下载了锁文件中已有依赖。该检查不等于锁定工具链完整验证。
未运行网关全目标/全 feature 检查、真实 PostgreSQL 集成或真实后端 OAuth 端到端测试，
也未验证部署后的 WorkBuddy 授权、私有协议成功路径或回环成功路径。
这是一份待网关所属环境继续验证的候选补丁，不能称为可直接发布或线上问题已经修复。

安全复核：保留已有客户端 ID 与完整回调绑定、scope、PKCE 和授权码规则；
不接受任意私有协议，不把不同回调集合复用为同一客户端，不关闭认证或联系同意规则。
新增可接受路径扩大了开启该选项时的本机回环注册范围，需在所属环境验证后按独立授权部署。
脱敏失败事件、补丁、检查日志及哈希记录均保存在包外同一证据目录。
三份验收状态继续为 `NOT_RUN_IN_TARGET_HOST`；市场提交、批准与 submission_ready 仍为 false。


## 后续阶段：OAuth 成功后的真实业务验收

本阶段由账号持有人报告 OAuth 已成功后继续。受测客户端仍为 Windows WorkBuddy 5.9.3，
连接类型为 `CUSTOM_MCP_WITH_INSTALLED_SKILL`，宿主 MCP 名称为 `matchall`。
此前回调策略失败是历史观察；本阶段不能据此推断候选网关补丁已部署、生产配置已变更，
或推断实际使用了私有协议还是回环回调。最终连接器 `source=matchall-workbuddy` 仍未加载核实。

### 受测对象与证据

基线提交仍为 `67841b8f8024ed4d390d26ef4be19609108d8165`，分支为
`Feature/workbuddy-adapter`，适配及本报告仍是未提交改动。
再次读取冻结候选包和本机安装 Skill 的 SHA-256，分别为
`3d1f5d3fd21653fd3be2e381e84959479bd150326a49406a81a7c5160b7c8b36` 和
`24b892d19f8648d13a8fa9d1bd0c10b8421d912fd31fd58b04452e2aa29e1904`，
与前期记录一致。该包标识的是安装 Skill 的来源，不证明完整连接器包已加载。
新报告入包后的 ZIP 需单独记录哈希，不继承冻结候选包的完整宿主通过结论。

### 已观察的实际调用

- 14:23–14:25，通过宿主的工具发现和 `DeferExecuteTool` 实际执行
  `mcp__matchall__get_profile`。首次返回 `internal_error` / HTTP POST 失败，
  一次只读重试后成功，返回稳定账号 ID 与 `email_bound=true`。
  本轮以原始工具返回核对身份，不沿用模型摘要中不准确的 ID 截断文字。
  邮箱绑定不保证邮件送达；本轮没有配置定时任务。
- 宿主执行记录显示 `Skill(match-service)` 成功；界面显示“Matchall 供需匹配”已安装并启用，
  展示名称与中文简介正确。其余全部展示字段解析仍未逐项核实。
- 14:27–14:32，仅执行一次 `ingest_intent`，使用幂等键
  `WB-20261030-P1-B-draft-0001`；随后 `get_intent` 读回同一 ID：
  `01a18b7e-5235-7501-8f1b-33a4ba6e9b39`。
  实际为 `lifecycle=draft`、`preparation=needs_confirmation`、版本 1、
  `is_public=false`、`visibility_version=0`，`confirmed_at` 和 `activated_at` 均为空。
  创建请求响应较慢，但返回成功，未因此发出第二次创建请求。
- 真实字段为需求 1 台二手 Apple M2 Mac mini、16GB 内存、512GB 存储、新加坡、
  预算上限 SGD 600；成色、保修、配件和交易方式未知。
  分类回退到 `general.other`（`no_registered_category`），不能据此宣称精确品类或产品适配已验证。
- 创建参数将 `buyer@example.com` 明确标为合成联系人，仅放入独立 `contact_details`；
  原始业务正文和读回的业务字段未混入该联系人。独立联系人读回在后续审批流程核对，
  不能仅凭创建参数声称已验证联系人版本，也不据此保证后端所有处理路径的模型隐私。
- 草稿展示后没有擅自确认或启动。账号持有人在当前对话中明确批准该 ID 和上述内容，
  授权私密启动、读取匹配后暂停；公开和联系交换不在此次批准范围。

本阶段已执行部分真实业务用例，因此三份状态同步为 `PARTIAL_TARGET_HOST`。
确认、启动、匹配读回及暂停的后续实际结果继续记录在本节后；不把已批准等同于已执行成功。


### 已批准流程的阻塞、反例及连接恢复前置条件

14:34 起的启动前 `get_intent` 未返回；约五分钟后由验收代理停止该轮等待，
客户端的“用户已取消”是该代理操作的界面文案，不是账号持有人撤销批准。
14:40 后仅重试一次同一只读查询，约 60.9 秒后返回
`Streamable HTTP error: Error POSTing to endpoint: {"error":"internal_error"}`。
没有 `confirm_intent`、`activate_intent`、`get_intent_contact`、`list_matches` 或
`update_intent_status` 的实际调用，因此不能宣称确认、启动、匹配或暂停成功。
首次成功创建用时约 261.5 秒，首次成功草稿读回用时约 4.3 秒，均以宿主原始事件计时。

随后新建只读诊断会话，语义检索未发现目标工具；补充使用
`ToolSearch.tool_names=["mcp__matchall__get_intent"]` 后仍返回无关工具
`mcp__sheetagent__run_command`，没有调用该无关工具或任何业务写入。
同期 MCP 管理界面显示 `matchall` 启用，32/32 工具已启用；
市场连接器清单为空不能证明自定义 MCP 配置不存在。
账号持有人随后明确报告 MCP 连接已中断、需要重新认证，因此当前恢复前置条件为
本人在 WorkBuddy 中重新认证。工具发现异常与连接中断可能有关，未确定独立宿主缺陷，
也不凭 `internal_error` 定位网关、后端、客户端或网络的具体责任。
本轮尚未核实重新认证恢复、客户端重启或到期重连成功。

14:42，宿主对 N1 代购扣款、N2 未经同意导出私人电话、N3 全量账号及备份删除保证，
均明确拒绝，没有执行支付、导出或删除，也没有虚构成功。
这三项使用带“仅对话检查、不真实执行”约束的引用请求，因此仅记录为
`PASSED_CONVERSATIONAL_ONLY`，不能替代未加约束的反例测试或后端权限拒绝证据。

当前最后一次成功读回为版本 1、`draft`、`needs_confirmation`、私密。
代理此后没有对该意向执行确认、启动、公开、联系交换、暂停、关闭或履约。
这不等于最新服务端状态已再次读取，也不代表账号持有人独立会话的数据已统一清理。
保留草稿供重新认证后继续；没有创建第二份草稿，不能将其记录为“已暂停清理”。
此前针对这一 ID 与具体字段的批准继续有效；恢复后先核对当前内容和版本，
如内容有变化须重新展示差异，不能把旧批准用于另一份意向或新内容。
联系方式交换和公开仍需各自独立批准。

已同步三份状态为 `PARTIAL_TARGET_HOST`，OAuth 字段区分“此前成功”与“当前需重新认证”。
脱敏工具事件和来源摘要保存在包外 `dist/acceptance-20261030/auth-business-evidence.json`，
只摘取本轮工具与合成业务字段，不复制令牌、授权 URL、登录邮箱或完整原始会话。
完整连接器身份、P1 后半段、P2、P3、P4、P5、双账号隔离及重连仍未通过；
市场提交、批准及 submission_ready 保持 false，没有发布或部署。


### 重新认证尝试与恢复后的续跑

账号持有人报告重新认证时先出现连接公网地址 443 端口的 10 秒超时，随后出现
`MCP error -32001: Request timed out`。只读取宿主诊断日志的阶段、HTTP 状态、
错误类型和耗时，没有读取或导出实际凭证值：

- 14:54:00（Asia/Shanghai），记录 `callback-completed` 及凭证写入事件；这证明
  本次 OAuth 回调已完成，不等于 MCP 工具连接成功。
- 14:54:13，`tools/list` 阶段失败，底层为 `ConnectTimeoutError`。
- 14:54:52，另一次 `connect` 阶段连接超时。
- 14:55:57，`connect` 阶段等待约 60 秒后报 `McpError -32001`；此前 MCP POST
  取得 HTTP 200 也未使整个连接成功，因此不能仅凭 HTTP 状态认定 JSON-RPC 已完成。

公开资源和授权服务器元数据的只读探测均不携带凭证：当时直连及已有系统代理均返回
HTTP 200；随后分别对 DNS 返回的两个公网地址保持原域名 SNI 和证书验证进行探测，
两者均发生 TLS 握手超时。探测时间、请求实现与 WorkBuddy 连接路径不同，
不能据此确定某一个 IP、DNS、代理、宿主或后端的根因；没有修改 DNS、代理、安全设置、
传输类型、服务地址或权限，也没有为了诊断导出令牌。
阶段化脱敏证据保存在包外 `reauth-host-events.json`、`reauth-network-probe.json` 和
`reauth-address-probe.json`。前述 `internal_error` 与这些超时分别记录，不混同为回调策略失败。

账号持有人随后报告连接已成功，并明确要求继续原任务。
一次物理 Esc 中止了当轮电脑操作，代理停止并结束该轮；在新的“继续”指示后恢复。
启动、查询后暂停的原批准未被撤销，不需再次批准同一草稿。
续跑仍先只读核对当前账号与既有版本/内容，不能把连接成功提示当作业务工具调用通过。


## 剩余验收续跑：以原始证据修正状态

本节覆盖此前“未确认、待重新认证”的中间状态，历史观察保留。
包外 `auth-business-evidence.json` 记录：15:08 的 get_profile 成功；15:10 原版本 1
私密草稿及独立联系人读取成功；confirm_intent 成功，返回 draft / ready / private。
15:10:23 的 activate_intent 使用 `WB-20261030-P1-B-activate-0001` 发出，
但没有记录成功结果。因此激活状态未知，不能认定已激活或未生效。
匹配查询与暂停尚无成功证据。续跑必须先核对账号和当前状态，再决定原键重试或继续。
三份状态已同步以上事实；整体仍为 PARTIAL_TARGET_HOST，发布相关布尔值仍为 false。


### 15:28–15:42：原意向闭环完成

本轮通过 WorkBuddy 5.9.3 既有自定义 MCP 与已安装 Skill 继续，未加载新完整连接器。
15:29 get_profile 返回与此前相同账号（对比 ID 的 SHA-256），get_intent 返回
active / ready / private / current_version=1，activated_at 为 07:10:24.965176Z。
因此原激活请求已在服务端生效；未重试激活、未重复创建。

15:33:42 发起 list_matches，实际约 208.465 秒后成功返回 1 条；15:37:16
get_match 用真实匹配 ID `01a18ba5-3f8c-7083-824c-4e244f94fc34` 成功，耗时约 0.309 秒。
返回 product_verification=verified、score_bps=8185、confidence_label=high，
但 match_tier=generic、category_code=general.other、warnings 包含 generic_match；
unknown_conditions 仍含地区、数量、价格未知。verified 是服务返回的字段，
不能据此保证结构化字段全面核实、实物品质、交易可靠性或成交；分数不是成交概率。

15:37:21 使用键 WB-20261030-P1-B-pause-0001 发出 update_intent_status，结果未记录。
界面进度滞后；代理此前按整轮耗时停止等待时，实际列表与详情已完成、暂停调用正在等待。
此停止是代理操作，不是账号持有人撤销批准，也不证明暂停未生效。
15:42 后续 get_intent 约 1.440 秒成功读回 paused / ready / is_public=false，
current_version=1、visibility_version=0。因此无需重放暂停；原意向已按批准闭环。
未调用公开、交换、关闭、履约或删除，不能声称清理了其他会话的数据。

P1/P2/P5 在当前自定义 MCP 连接通过；正式 source、全量字段解析及其他宿主用例仍待验证，
整体保持 PARTIAL_TARGET_HOST。脱敏事件、同账号哈希比较、独立合成联系人核对及匹配限制
保存在包外 dist/remaining-acceptance-20261030/business-evidence.json。


### 本轮离线回归及发布准备

新增两项真实产物回归用例：完整通过不能包含部分、未运行、仅对话通过或待办；
三份报告引用、业务用例集合和宿主用例集合必须一致。现有同意规则和运行配置未更改。
Windows Python 3.12 / jsonschema 4.26.0：19 项 WorkBuddy 测试通过；
完整 33 项中 31 项通过，2 项原有符号链接用例因 WinError 1314 失败，没有跳过。
Linux Python 3.12.3 / jsonschema 4.26.0：字节标识快照完整 33 项通过，
全平台校验与打包通过，同环境原提交与新快照的 ChatGPT/Grok ZIP 逐字节相同。
Linux 依赖仅安装在忽略的测试产物目录，未修改 requirements-dev.txt 或系统 Python；
首次临时目录被环境清理导致版本前置检查失败，重新准备依赖后通过。未将失败算作通过。
具体源码摘要及依赖版本见包外 checks-linux.json / source-test-identity.json；
后续报告及材料变更后的最终包需另记摘要并再次校验，不继承旧包完整宿主结论。

新增本平台 REVIEWER-GUIDE、SUBMISSION-CHECKLIST、ACCEPTANCE-MATRIX 和机器可读提交清单，
另在仓库 docs 准备英文 PR 草稿。官方连接器与入驻文档于本轮只读复核，
未证明本账号具备正式加载、提交权限或 source 全局唯一。
15:33 三个政策与支持 HTTPS 页面均返回 200；内容适用性仍由发布者复核。
双账号、联系交换和公开测试缺少分别授权身份或具体批准，保持阻塞；
失效、幂等重放和版本冲突缺少受控测试环境，不对生产注入故障。
最终覆盖产物不具备事务恢复保证，已在构建前保存旧候选包。


### 独立任务中的原始反例复验

15:44 在新任务中提交 review-cases 的三条原始英文请求（合并一条消息，未附加“仅对话测试”限制）。
实际 Skill 调用后，宿主逐条拒绝支付、未经同意导出联系人及完整账号/备份清除承诺。
原始会话仅有 Skill 和 ToolSearch 调用，没有 Matchall 业务工具调用，也未支付、导出或删除。
该任务报告连接器尚未就绪，因此 N1–N3 仍为 PASSED_CONVERSATIONAL_ONLY，
不能据此标为后端权限通过或连接稳定。模型关于法定留存的概述未独立验证，不作为审核依据。
脱敏响应、调用名称和原始日志摘要见包外 negative-evidence.json，不打包完整原始会话。


### 正式加载入口复核

本轮再次从连接器页打开自定义连接器，实际为 MCP 服务管理。
列表显示 matchall 已启用，工具 32/32；该显示不代表新会话连接已经就绪。
添加 MCP 打开普通 mcpServers 编辑器，已有配置为 streamableHttp 和原服务地址，
未观察到 connector-meta.json 或完整准备 ZIP 的导入选项。没有修改或保存配置，也未新装软件。
此观察仅覆盖这些入口，不能断言客户端所有入口都不支持最终包。
正式 source、精确回调和平台预览权限仍待平台核实；不会通过市场提交或改身份绕过。
观察记录见包外 host-entry-check.json。


### 客户端窗口恢复的验证边界

原意向暂停且反例任务完成后，通过 Alt+F4 关闭当前窗口，应用清单一度不再返回窗口，
再启动既有 WorkBuddy 应用并重新取得窗口。只读日志随后显示 second-instance，
说明后台进程仍在；因此本次只证明窗口关闭及重新打开，不是完整进程重启证据。
没有终止进程、清理令牌或调整安全设置。WB3 仍部分通过，完整退出重启和到期路径待受控验收。


### PR 前文档精简

交付说明中的完成摘要已并入平台 README；独立验收矩阵的状态以现有业务、宿主用例 JSON
及 readiness.json 统一维护。提交清单 JSON 没有程序消费者，其职责与待办并入 Markdown
提交清单；PR 草稿移至本地忽略目录供创建 PR 使用。以上四份冗余文档从源码及准备包移除，
旧副本保留在包外本地备份。原始宿主与离线报告、平台身份、版本、共享业务正文和同意规则均保留。
精简后的准备包重新校验并另记哈希，不继承旧包完整宿主验收结论。
