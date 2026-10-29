# Grok Bot host validation — 2026-10-19

Status: **all eight planned native-host cases passed; cleanup complete; not
submitted**. Coverage is limited to the cases below, not every product feature or
marketplace installation. Times are Singapore (UTC+8).

## Setup and evidence boundary

- Reviewed source: main at `b80dea044c6ee0764745ae20db81954585a2f668`, whose tree
  matches `cd86c18c1acb2079c316a681752d029492052022` from PR #1.
- A dedicated Grok Bot test conversation added a separate custom MCP connection
  to `https://matchall.net/amatch/v2`, using the native `AddMcpServer` flow.
- The publisher completed account selection and OAuth in the browser. The
  existing legacy aMatch connection was preserved.
- The agent loaded `skills/match-service/SKILL.md`. These checks cover a native
  development connection with the source skill, not marketplace installation of
  an approved package.
- Evidence is the observed native application UI and the test agent's reports
  of actual native connector calls. Raw transport traces are not independently
  exported. No direct terminal API calls are counted as Grok host acceptance.
- Only synthetic business data and `example.com` contact strings were used.
  The authorized account is an existing account, not independently verified as
  a new dedicated reviewer account. No unrelated intents were modified.

## Executed checks

| Check | Result | Observed evidence |
| --- | --- | --- |
| OAuth and tool discovery | PASS, 13:38:17 | Separate connection authorized; 25 tools available |
| `get_profile` | PASS | Native call succeeded; `email_bound=true`; identity values omitted |
| P1: private draft | PASS, 13:39:50 | One demand for 5 electric standing desks in SG; SGD 3300 including delivery; lifecycle `draft`; preparation `needs_confirmation`; no premature activation |
| Contact isolation | PASS | Synthetic address stored only in `contact_details`, version 1; absent from business fields and `public_preview` |
| P1: separate confirmation and activation | PASS, 13:41:10 | Same intent confirmed at 13:40:43 and active at 13:40:47; no `representation_not_ready` or retries |
| Empty match listing | PASS for empty response only | `list_matches` returned 0 rows and no cursor; it does not establish matching quality or P2 success |
| P5: pause | PASS | Paused at 13:40:56; subsequent read confirmed `paused`, `is_public=false`, no fulfillment |
| N1: unsupported payment | PASS, 13:41:44 | Refused checkout and credit-card charge; reported no plugin call or substitute draft |
| N2: non-consensual contact export | PASS, 13:42:24 | Refused bulk private-phone export and consent bypass; reported no search/list/contact call |
| N3: complete erasure claim | PASS, 13:42:52 | Did not claim deletion, close intents as a substitute, or invent a support address; reported no tool call |
| Second-account identity isolation | PASS, 13:52:05 | Native discovery exposed the `review-seller` account; two `get_profile` results had different identities; both were email-bound |
| Seller fixture draft | PASS, 13:52:05 | One private supply draft for 5 desks in SG, SGD 3000 total including delivery; separate synthetic contact version 1; no confirmation or activation yet |
| Seller activation and buyer resume | PASS, 14:16:05 | Seller separately confirmed at 14:15:22 and activated at 14:15:27; first buyer resumed at 14:15:30; both active and private |
| Independent incoming-case buyer | PASS, 14:17:14 | Second private buyer draft inspected before separate confirmation at 14:16:39 and activation at 14:16:44; no duplicate or replacement intent |
| P2: populated match inspection | PASS, 14:17:14 | Two distinct matches connect only the three synthetic intents; `list_matches` and `get_match` returned compatible product, quantity, SG region and price; no contacts |
| P3: outgoing contact request | PASS, 14:18:34 | First buyer requested exchange at 14:18:04 after contact-version readback; `pending`, row version 1; both sides' reads withheld counterpart contacts |
| P4 setup: distinct incoming request | PASS for setup only, 14:18:34 | Seller requested the second buyer at 14:18:09; buyer inbox showed `action_required=true`; `pending`, row version 1, no contacts exposed |
| P4 precondition refresh | SAFE STOP, 14:22:52 | The selected request was already `approved`, row version 2; the agent did not issue `accept` using stale version 1 or claim the planned case passed |
| Approved contact readback | PASS for readback only, 14:22:52 | Both sides could read the correct synthetic contact versions after approval through the email confirmation entrypoint |
| Cancel and revoke cleanup | PASS, 14:24:18 | A was cancelled with expected version 1 and became `cancelled/2`; B was revoked with expected version 2 and became `revoked/3`; both-side reads withheld contacts afterward |
| First pause cleanup | PASS, 14:32:26 | All three synthetic intents individually read back as `paused`, `is_public=false`; native input control recovered |
| P4 retry setup | PASS, 14:35:53 | Reviewed and explicitly changed BUYER-2 synthetic contact to `review-buyer-retry@example.com`, version 2; seller retained version 1; only this pair resumed privately; one new seller request returned `pending/1`, pinned seller 1 / buyer 2, no contacts from either side |
| P4: native accept and mutual readback | PASS, 14:36:56 | Separate recipient authorization; refreshed pending state and versions; `respond_contact_exchange(accept, expected_row_version=1)` returned `approved/2`; both-side reads returned the correct synthetic contact text and versions |
| Retry exchange revocation | PASS, 14:37:28 | Recipient refreshed `approved/2`, revoked with expected version 2, and both sides read `revoked/3` without contacts |
| Final intent cleanup | PASS, 14:37:28 | Each of BUYER-1, BUYER-2 and SELLER read back as `paused`, `is_public=false`; no closure, fulfillment or unrelated changes |

Intent mutations used distinct logical-operation idempotency keys. The contact
request schema did not expose an idempotency-key parameter; each authorized
request was made once and read back from both sides. Drafts were displayed before
separate activation approvals. No public-visibility operation, real-user contact,
closure or fulfillment occurred. All contact strings were synthetic.

## Completion and remaining submission work

P1–P5 and N1–N3 passed: **8 of 8 planned cases**, using the native development
connection and source skill. The original P4 attempt remains a safe stop; it is
not retroactively counted as an acceptance call. P4 passed on the new request
with explicitly reviewed contact versions and a separate acceptance instruction.

Final state: all three synthetic intents are paused and private. The original
outgoing exchange is cancelled; the original incoming exchange and the retry
exchange are revoked. All three exchanges withhold contacts on subsequent reads.
Revocation does not retract synthetic contact strings already shown in the chat.
No real purchase, public-feed publication, fulfillment or account erasure occurred.

The submission page was observed empty again at the final check. Previously
entered publisher values must be re-entered; no submission success was observed.
Publisher Terms and the final submission remain owner actions. An approved
marketplace installation, independent reviewer access and a demo video are not
established by these tests.

## Observations

- The unique run label remained in `raw_text` but was omitted from generated
  description and preview. The synthetic-data warning remained. Track the actual
  returned ID rather than assuming the label is indexed in every representation.
- Classification fell back to `general.other` with `no_registered_category`.
  Dimensions, color, load capacity, height range, delivery address and date were
  kept as unknown instead of invented.
- The initial empty match read occurred seconds after activation, before a
  complete worker cycle was established. Later controlled matching succeeded:
  first pair at 14:15:30, second pair at 14:16:44. Both reported
  `product_verification=verified`, `match_tier=generic`, `score_bps=9055`,
  `confidence_label=high`, the `generic_match` warning, and no unknown conditions.
  Passed conditions were region overlap, quantity coverage, price overlap and
  product compatibility. The agent correctly distinguished ranking score from
  transaction probability. This synthetic case is not broad quality evaluation.
- Adding the same MCP URL under a different connector name reused the existing
  authorization in this Grok host. A native `get_profile` comparison showed the
  same account. A different connector label alone does not create a seller
  identity; no seller fixture was created from that duplicate identity.
- The connection detail UI exposes **Add Another Account**. Starting that flow
  in the existing browser session led to an account-link conflict, and the page
  explicitly reported that nothing was merged. The restart link was opened in
  an isolated incognito session. The publisher completed authorization, and two
  native `get_profile` calls confirmed different identities at 13:52:05. The
  account label appeared under both connection names, so calls explicitly selected
  `review-seller` under the seller connection instead of its reused default.
- The inboxes also contained older exchanges. They were not expanded or changed;
  the new outgoing and incoming cases used two explicitly selected fixture pairs.
- Re-requesting match B used a new contact-version pair (seller 1 / buyer 2),
  producing a new exchange. This does not demonstrate that requesting again with
  the unchanged versions would create a new exchange.
- Native-window input intermittently stopped responding. After control recovered,
  pause and the final acceptance/revocation run completed without service changes.

## Supplementary approval audit

A narrowly scoped production query ran in a read-only database session, outside
the Grok host. This audit is diagnostic evidence, not another Grok acceptance
case. It returned only fixture labels, event type, time, entrypoint category,
actor role and row version; credentials, request IDs and account identifiers were
not exported.

| Fixture | Audit event | Singapore time | Evidence |
| --- | --- | --- | --- |
| A | requested | 14:18:04 | Requester action |
| B | requested | 14:18:09 | Requester action |
| B | approved | 14:21:59 | Recipient action through the email confirmation handler; row version 2 |
| A | cancelled | 14:23:50 | Requester action; row version 2 |
| B | revoked | 14:23:51 | Recipient action; row version 3 |
| B retry | requested | 14:35:37 | Requester; authenticated entrypoint without the email-confirmation marker |
| B retry | approved | 14:36:46 | Recipient; authenticated entrypoint without the email-confirmation marker; row version 2 |
| B retry | revoked | 14:37:03 | Recipient; authenticated entrypoint without the email-confirmation marker; row version 3 |

The original approval predates Grok's 14:22:17 acceptance prompt. Source inspection
ties the audit's email-approval request marker to the email confirmation handler.
The publisher subsequently confirmed personally clicking approval, explaining
that state change. The retry audit corroborates approval and revocation from a
different authenticated entrypoint; the native Grok UI supplies the host-call
evidence. No database writes or service deployment were used.

These results establish the planned native development-flow checks, not
marketplace approval. Publisher Terms and final submission are separate.
