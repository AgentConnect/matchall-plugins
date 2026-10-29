# ChatGPT MCP endpoint — October 22, 2026

Deployment history: **0.1.5** used **https://matchall.net/mcp/chatgpt**.
The portal subsequently rejected that URL change for the existing draft.
Current package **0.1.6 restores https://matchall.net/amatch/v2**. The new alias
remains deployed, but should not be uploaded as this existing app's MCP URL.

The owner explicitly authorized this endpoint deployment. It is an exact OAuth
resource alias for the same Matchall account/data service. The original
https://matchall.net/amatch/v2 endpoint remains available, and the OAuth issuer
remains https://www.amatch.me/oauth/match. This does not create a separate data
store or grant additional tool permissions.

The new protected-resource document is:
https://matchall.net/.well-known/oauth-protected-resource/mcp/chatgpt

## Observed acceptance

- Public HTTPS discovery identifies the new resource and retains live issuer/scopes.
- Both HTTP 401 and anonymous tool-level OAuth challenges point to the new document.
- Invalid bearer tokens and untrusted browser origins are rejected.
- Synthetic public-client DCR, PKCE authorization, token exchange and refresh pass.
- Authorization-code and refresh exchanges reject a different resource audience.
- Authenticated tools/list returns **32 tools**; get_profile succeeds using fresh
  and refreshed tokens. The old endpoint still works with the same account.
- All issued diagnostic connections were revoked and their access tokens rejected.
- No business intents, contact exchanges or participation records were created;
  no verification emails were sent. A diagnostic client and email-free test
  account remain as audit records. They are not dedicated reviewer credentials.

The OAuth check used an allowed IP-literal loopback callback and a synthetic
account, not the OpenAI submission portal. An arbitrary unregistered callback
was rejected as expected; the callback policy was not expanded. Machine evidence
is in `chatgpt-endpoint-check.json`.

## Administrator next steps

Upload the complete 0.1.6 ZIP on the existing Matchall entry. Confirm that MCPs
retains the original URL. Resolve the original organization binding conflict
with support, then complete the portal's domain verification, OAuth
connection and fresh tool scan. Support/privacy/terms and the demo URL remain
included. Dedicated reviewer access and all eight target-host cases remain open.

The latest user-provided screenshot confirms this existing draft rejects MCP URL
changes. The server-side deployment does not resolve the original organization
binding conflict. Contact OpenAI Support with both error messages and the existing
plugin identity; do not delete the app or claim successful submission. Portal
operations remain with the administrator; no successful upload, verification,
scan or submission has been confirmed for this change.
