# Grok Bot submission readiness

Checked 2026-10-19. **Preparation only; not submitted, listed or approved.**
Use [the form draft](grok-submission.json), [submission guide](GROK-SUBMISSION.md),
[status](readiness.json), [review cases](review-cases.json), and the
[dated host validation report](host-validation-2026-10-19.md).

## Confirmed

- Public repository: https://github.com/AgentConnect/matchall-grok-bot.
- Native Cursor plugin structure with a skill, MCP configuration and MIT license.
- Current product homepage: https://matchall.net.
- Current dedicated MCP endpoint: https://matchall.net/amatch/v2.
- Public OAuth metadata identifies that exact resource and intent:read / intent:write.
  The advertised issuer's discovery endpoint returns PKCE S256 and dynamic
  registration metadata. Anonymous initialize/tools/list return 401.
- Existing 512 × 512 white-backed PNG logo is publicly readable and matches the
  local asset. No new logo, release or hosted policy was published.
- The official Grok form accepts a public repository or MCP URL, with separate
  options for Grok Bot, Cursor and Grok (coming soon).
- PR #1 merged into main at `b80dea044c6ee0764745ae20db81954585a2f668`.
  Its tree matches the reviewed source revision `cd86c18`, whose CI passed.
- Publisher identity fields were previously supplied directly, but the final
  page inspection showed all inputs empty. They must be re-entered before
  submission; personal values are not retained in this public repository.
- A separate Matchall connection was added through Grok Bot's native custom MCP
  flow. OAuth, discovery of 25 tools and native `get_profile` succeeded.
- Two different account identities were verified. P1–P5 and N1–N3 all passed:
  private drafts, separate activation, populated controlled matches, pending
  privacy, native acceptance with correct mutual contact readback, pause and
  unsupported-request boundaries. All three synthetic intents finally read as
  paused and private; cancelled/revoked exchanges withheld contacts.
- The original P4 request was approved by the publisher through email before
  Grok acted. Grok correctly stopped on changed state. A fresh, independently
  authorized request then passed native acceptance.

## Required before submitting this preparation

1. Refill the currently empty submission form and have the publisher verify its
   identity fields. Prepared public values are in the form draft.
2. Consult the dated report when attesting to testing: all eight planned cases
   passed on a native development connection with the source skill. This does
   not establish marketplace installation or every product feature.
3. At an authorized submission step, the publisher reviews and accepts the
   Publisher Terms. Preparing code/materials does not submit the form.

## Additional preparation, not verified form fields

The inspected form does not ask for a ZIP, country list, commerce declaration,
demo URL or four separate listing URLs. Do not treat OpenAI portal metadata,
test-case counts or reviewer email addresses as Grok requirements. Keep review
cases, demo plans and access instructions for follow-up. A real recording,
reviewer access, private support and service policies remain unverified. Unknown
publisher, data-retention, deletion and commerce facts must not be invented.

## OAuth verification boundary

Discovery does not test client registration, actual Grok callback URIs, consent,
code exchange, refresh or tools. Check the current host's exact redirect request
and server allowlist if authorization fails; never introduce wildcard callbacks
or shared tokens. The stable issuer is https://www.amatch.me/oauth/match, while
public authorization/token/registration endpoints are on matchall.net. Existing
awiki.info accounts and connections are not silently migrated.

## Sources

- [Grok submission form](https://x.ai/bot/marketplace/submit-a-plugin)
- [Grok app connections](https://docs.x.ai/grok-bot/computer-and-apps#connect-an-app)
- [Cursor plugin format](https://cursor.com/docs/reference/plugins)
- [Publisher Terms linked by the form](https://cursor.com/marketplace-publisher-terms)
- [Matchall homepage](https://matchall.net)
