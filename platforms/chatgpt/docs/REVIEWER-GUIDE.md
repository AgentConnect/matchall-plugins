# Matchall ChatGPT review preparation

Candidate 0.1.10; preparation only. The existing MCP URL remains
https://matchall.net/amatch/v2. No successful run of all eight cases in the final
packaged ChatGPT installation is claimed.

## Reviewer access

The current submission portal explicitly supports **Magic link or email code**.
Its designated reviewer mailbox has been pre-provisioned as a dedicated Matchall
account. Enter its address and sign-in instructions only in secure portal fields,
not in this ZIP. The reviewer receives and enters their own code; owner mailbox,
phone, Google account and a second reviewer mailbox are not required. Reviewer
mailbox delivery and actual reviewer sign-in have not been observed. Preparation
did not send a code to the reviewer, read their mailbox or provide session cookies.

This supersedes earlier preparation notes prohibiting all email-code sign-in.
The user supplied screenshots of the supported method and exact designated email.
The operator-controlled seller is only a synthetic fixture; reviewers never need
to sign in to it or obtain its approval to run this case set.

## Provisioned samples and repeatable cases

A dedicated buyer and separate seller contain synthetic M2 Mac mini samples,
16 GB RAM, 512 GB SSD, working condition, proof of purchase and Singapore
collection. Buyer budget: SGD 600; seller price: SGD 550. The samples are active
and private. Their business descriptions include REVIEW-20261022-SG-MINI-PENDING
and REVIEW-20261022-SG-MINI-PENDING-SELLER. Current extracted display titles may be
shorter: identify the seller using its actual business description and ID.

Synthetic private contact strings are review-buyer@example.com and
review-seller@example.com. Neither is a receiving mailbox or login credential.
Initial sample expiry is October 22, 2027; the operator must refresh the samples
before expiry for later reviews. No automatic maintenance is claimed.

Backend setup verified an actual matching result, contact withholding while
pending, and cancellation without contact disclosure. Historical cancelled setup
exchanges may appear in the pre-seeded buyer account. They are not the new test
run. These backend checks do not mark the following ChatGPT cases as Passed.

Run docs/review-cases.json in sequence:

1. P1 creates a NEW private buyer intention with a unique REVIEW-NEW label. Inspect
   the draft and separate contact; only a separate approval turn permits confirm
   and activate. Do not reuse the pre-seeded buyer or a previous test intent.
2. P2 finds the actual pre-seeded seller match from that new buyer intention.
   Explain product verification and unknowns accurately; scores are not transaction
   probabilities. Never select unrelated real counterparties.
3. P3 requests conditional contact sharing for that exact synthetic match. The
   seller has not consented; its private contact must remain unavailable.
4. P4 cancels that pending request using its current row_version, then verifies
   status and contact withholding. Do not accept on behalf of the seller.
5. P5 pauses only the NEW P1 buyer intention. Preserve the pre-seeded samples.
6. N1 payment, N2 unauthorized contact export and N3 complete-erasure claims
   should explain limits without substitute writes or fabricated outcomes.

Repeat with a fresh P1 intention. Cancelled exchanges intentionally cannot be
reopened for the same match/contact versions. Do not silently change contacts,
invent renewed consent or delete audit history to reset a test.

## Recording and acceptance limits

Direct recording: https://matchall.net/review/matchall-chatgpt-demo-20261023-narrated.mp4
Player/context: https://matchall.net/review/matchall-chatgpt-demo-20261023.html

The approximately 7:01 video records October 22 ChatGPT development MCP
interactions for all five positive and three negative cases. Login, unrelated
windows, waiting intervals and original audio were removed. English AI narration
and optional English captions were added October 23; actual video is unchanged. Two actual source frames are
explicitly held for reading. The public MP4 was checked for anonymous playback
and seeking. See DEVELOPMENT-REHEARSAL-20261022.md for observed results and limits.

This is not final-package acceptance. A standard fresh-account OAuth request
still includes an incompatible scope; the recorded session used a narrower
user-authorized request. Repair and retest normal connection before acceptance.
Reviewer-mailbox delivery and sign-in also remain unverified.

## Portal handoff

The administrator operates the existing draft. Upload the new ZIP to import the
revised cases, preserve the original MCP URL, and verify all imported fields.
Supply reviewer access only in secure Review details fields and save them.
A user screenshot shows MCP Configured/account connected; the annotation fix was
deployed separately and a fresh portal Rescan result remains to be checked.
Verify publisher/domain/security requirements and run all eight cases against the
saved package. The authorized publisher completes attestations and submission.
