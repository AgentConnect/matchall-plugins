# Matchall：MCP 绑定冲突与禁止修改 URL

更新：2026-10-22。门户截图已经确认：**当前未发布草稿也禁止更换 MCP URL**。
当前准备包 **0.1.6** 恢复 `https://matchall.net/amatch/v2`；保留 Support、Privacy、
Terms 和演示链接。它修正包内地址不一致，但不能自行解除门户内部的绑定冲突。

## 已有证据

| 操作 | 观察结果 |
| --- | --- |
| 在原 Matchall 条目保存原 MCP URL | This MCP URL is already used by another app in your organization. Use a unique MCP URL for each app submission. |
| 上传改用 /mcp/chatgpt 的 0.1.5 | MCP URL must match the existing app；要求恢复原 URL |
| 提交者说明 | 没有提交过其他应用，一直在同一页面上传新版本 |
| 配置比较 | 0.1.2、0.1.3、0.1.4 使用原 URL；0.1.5 是唯一改为新入口的已交付版本；0.1.6 恢复原 URL |

原入口持续保留，新入口已经部署并通过协议测试。服务端可用不代表门户会接受
更换 URL。组织内具体占用记录尚未识别，不能断言提交者重复创建应用，也不能
断言一定是 OpenAI 残留记录；需要支持检查插件与内部 MCP app/server 的关联。

## 管理员下一步

1. 在原有正确 Matchall 条目选择 Reupload ZIP，使用 0.1.6 完整恢复包。
   核对保存的 MCP URL 是原地址，政策、视频等字段仍完整。0.1.5 不再用于该条目。
2. 如 MCP 详情仍报组织内占用，把下方英文说明、两张脱敏错误截图、原插件页面
   链接和实际出错时间发给 OpenAI 支持。组织、项目、插件 ID 只在私有支持渠道提供。
3. 请支持查明哪个内部记录占用了原 URL，并说明保留现有应用身份的修复方式。
   不先删除应用，不假定删除草稿一定释放 URL，也不继续尝试换路径或反复重传。
4. 绑定解决后，再完成域名验证、OAuth、工具扫描和审核材料验收。

当前官方更新说明要求更换已有 MCP URL 时联系支持：
[Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission#update-your-published-plugin)。
最新截图把这一限制明确到了本次草稿。本文只准备材料，未代管理员发送支持消息。

## 可复制给 OpenAI 支持的英文说明

Subject: Matchall draft blocked by both duplicate MCP URL binding and immutable MCP URL

Hello OpenAI Support,

We are preparing the existing, unpublished Matchall plugin for review. We are
blocked by two conflicting portal findings:

1. Saving MCP details with the original URL returns:
“This MCP URL is already used by another app in your organization. Use a unique
MCP URL for each app submission.”

2. After deploying a real alternative endpoint and uploading package 0.1.5,
the Reupload draft dialog rejects it:
“MCP URL must match the existing app. Changing the MCP URL of an existing app is
not supported. Restore its original MCP URL and upload the ZIP again.”

The submitter has not submitted any other application and has consistently used
Upload new version on this same Matchall entry. Packages 0.1.2 through 0.1.4 used
the original MCP URL. Package 0.1.5 attempted the new URL and was rejected.
We have now prepared 0.1.6 restoring the original MCP configuration while keeping
the public support, privacy, terms and demo links. Its upload result is not yet
confirmed. Neither endpoint was removed and the existing plugin was not deleted.

Plugin/package name: Matchall / matchall-chatgpt
MCP server key: matchall
Original MCP URL: https://matchall.net/amatch/v2
Alternative endpoint rejected for this draft: https://matchall.net/mcp/chatgpt
Organization: [provide privately]
Project: [provide privately]
Existing plugin/app ID and dashboard link: [provide privately]
Time and timezone of each error: [provide actual timestamps]
Latest 0.1.6 restore-upload result: [provide result if already attempted]

Please inspect the existing plugin's internal MCP app/server association and
identify the record owning the original URL. Please help repair an incorrect or
stale binding, or explain the supported recovery procedure while preserving the
existing app identity and its connection/review history. We cannot resolve this
by changing the URL because this same draft explicitly rejects URL changes.
Please confirm the impact before any unlinking, deletion or migration.

Attachments: redacted screenshots of both portal errors. No passwords, OAuth
secrets, access tokens, cookies or domain verification tokens are included.
