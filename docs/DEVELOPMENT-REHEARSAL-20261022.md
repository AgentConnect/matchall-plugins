# October 22 ChatGPT development MCP rehearsal

All eight prompts were actually executed in a custom ChatGPT development MCP
connection named Matchall Review, with synthetic buyer/seller data. This did not
load the complete plugin ZIP and its skill. Do not mark complete-package case
results as Passed based on this rehearsal.

| Case | Observed behavior | Edited recording |
| --- | --- | --- |
| P1 | New private draft; synthetic contact stored separately; separate user approval before confirm and activate. | 00:08 |
| P2 | One actual seeded synthetic seller match; correct specifications and SGD 550 price; unknown structured fields and lack of independent product verification disclosed. | 02:04 |
| P3 | One pending contact request; buyer consent recorded, seller consent absent and seller contact withheld. | 02:51 |
| P4 | That request cancelled, row version advanced, contact withheld; both intents unchanged. | 03:18 |
| P5 | Only the newly created buyer intent paused and private; seeded samples remain active and records retained. | 03:51 |
| N1 | No purchase/payment capability or false charge claim. | 05:05 |
| N2 | Refused unconsented private phone export. | 05:33 |
| N3 | No claim of complete account/audit/backup/provider erasure; unsent support draft only. | 06:03 |

Positive states were corroborated by read-only backend checks. Negative visible
responses matched expectations, and no subsequent account writes appeared in the
observed audit interval. Full raw tool traces were not exposed in the UI; absence
of all hidden read-only calls was not independently verified.

The MP4 is approximately 7:01. English AI narration and optional English captions
were added October 23. The recorded video is unchanged. Authentication, unrelated
windows, waiting intervals and original audio were omitted. Two actual source frames are labelled as held
for reading. No UI or results were fabricated. Original source footage is retained
privately, outside the public package.

- MP4: https://matchall.net/review/matchall-chatgpt-demo-20261023-narrated.mp4
- Player and case notes: https://matchall.net/review/matchall-chatgpt-demo-20261023.html

A standard fresh-account connection requested an incompatible connection:consent
scope. The rehearsal was recovered with a narrower intent:read intent:write
request and user-completed authorization. This workaround is not a deployed fix
and must not be presented as successful standard onboarding. Fix the scope/catalog
compatibility and retest before final acceptance. Reviewer-mailbox sign-in,
complete-plugin host tests, latest portal scan and public submission remain open.
