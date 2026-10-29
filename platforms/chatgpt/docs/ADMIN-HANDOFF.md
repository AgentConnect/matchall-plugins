# Matchall ChatGPT：管理员交接

更新：2026-10-23。当前准备包 **0.1.10**。尚未上传该版或提交审核。
用户指定由管理员操作门户；仅使用正确账号下已有的 Matchall 草稿。

## 当前已完成

- Support、Privacy、Terms 已上线并写入插件配置。
- 原 MCP URL 保持 https://matchall.net/amatch/v2；不得修改已有草稿的 URL。
- 用户截图已显示 MCP Configured、Account connected、Not submitted。
- 三个公开工具的 openWorldHint 修复已部署并读回验证；门户 Rescan 待确认。
- 门户支持 Magic link or email code。指定审核邮箱已预置专用账号。
- 私密合成买卖样例已创建，实际匹配、待确认/取消后不返回卖方联系方式已核验。
- 0.1.7 更新五个正例：新建并激活私密草稿、查匹配、请求联系方式、取消请求、暂停。
  三个反例保留。一个审核账号即可运行，无需卖方登录。
- 0.1.9 为 10 月 22 日八项开发 MCP 录像补入英文 AI 配音与可切换字幕，约 7:01；匿名播放、非静音状态与字幕载入已验证。
- 五项正例有后台状态交叉核实，三项反例可见行为符合预期；完整工具跟踪并未全部取得。

账号说明只填门户安全字段，不能放入公共 ZIP。审核员实际收信和邮箱登录尚未
验证；本轮未向审核员发送验证码。后台样例准备不能代替 ChatGPT 内八项验收。

## 当前必须先解决的连接问题

标准“连接另一个账号”请求包含服务端不接受的 scope。本次排练通过用户授权的
窄 scope 请求临时恢复，不能作为正常 OAuth 已修复的依据。修复 scope/工具目录
兼容性并重测标准新连接后，再完成整包验收与最终提交。不要让审核员手改授权 URL。

## 本轮分类提示修订

0.1.10 把分类改为 `Business & Operations`，简介改为 `Match buyers and sellers`，
并用二手电脑买卖例子说明需求、供给、匹配与双方同意联系的主要流程。功能和账号权限不变。
这是基于当前用途的分类判断，不代表门户已接受；详情见 [分类说明](LISTING-CATEGORY.md)。

## 管理员现在操作

1. 在原草稿上传完整 0.1.10 ZIP，核对版本号、四个公开网址、视频和 5 正 3 反用例。
   新 P4 是取消买方待确认请求，不再依赖卖方登录接受请求。
   同时核对分类和中英文介绍；打开 Findings 的 Blocking 筛选，确认此提示是否属于阻塞。
2. 打开 Add review information，保留 Magic link or email code，填写我们单独交付
   的 Login URL、Tenant 和 Sign-in steps。核对预填审核邮箱后 Save details。
3. 在 MCPs 执行 Rescan，确认已部署的标注修复消除 finding。
4. 核对域名、发布者身份、安全检查、地区、商业声明及所有剩余 findings。
5. 用审核账号在最终保存的 ChatGPT 包运行八项用例并记录结果。每次 P1 新建
   REVIEW-NEW 意向；P5 只暂停这条，不操作预置样例或普通用户。
6. 核对 ZIP 已导入本次新录像；保存审核资料，并确认全部门槛完成后，由授权发布者完成
   声明并提交。尚未证明这些门槛完成，不能称为可提交或已提交。

## 公开资料

| 项目 | 值 |
| --- | --- |
| 运营者 | Zhang Yifan，United Kingdom，18+；平台身份验证单独确认 |
| 官网 | https://matchall.net |
| Support | https://matchall.net/support |
| 支持邮箱 | support@awiki.ai |
| Privacy | https://matchall.net/privacy |
| Terms | https://matchall.net/terms |
| 演示 MP4 | https://matchall.net/review/matchall-chatgpt-demo-20261023-narrated.mp4 |
| 视频说明页 | https://matchall.net/review/matchall-chatgpt-demo-20261023.html |
| MCP | https://matchall.net/amatch/v2 |
| 地区 | countries=[]，全部平台可用地区 |

7:01 视频来自 2026-10-22 开发 MCP 连接，覆盖当前 5 正 3 反用例；
不是包含 skill 的完整 ZIP 验收，也不证明标准新账号 OAuth 成功。公开政策如实披露保留/删除、18+ 准入及处理商/跨境
安排的实施和核实缺口，见 POLICY-IMPLEMENTATION.md。场景仍包含广泛意向，
必须如实评估 commerce 限制，不能因为撮合免费或支付在线下而跳过。

## 样例维护与历史

当前样例初始有效期至 2027-10-22；到期前需运营者续期。没有配置自动维护。
不共享 session cookie；不把 example.com 联系字符串当成登录邮箱。
已取消的同一匹配/联系版本不可重新打开，每轮测试必须新建 P1 意向。

历史上原 URL 出现组织绑定冲突，0.1.5 更换 URL 又遭门户拒绝。0.1.6 恢复原
URL，后续准备包继续保留。后续截图已显示 Configured；不把历史错误直接视作当前
阻塞，也不推断平台内部根因。若再次出现，参见 MCP-URL-CONFLICT.md。
域名 challenge 已单独部署；不要从 ZIP 放置或覆盖 token，确认门户验证状态。
