# Operator facts and outstanding decisions

Updated October 21, 2026. These facts do not substitute for developer verification
or the publisher's legal declarations in the OpenAI portal.

Confirmed by the operator:

- Individual operator name: Zhang Yifan; AWiki is the brand.
- Operator country/region: United Kingdom, explicitly confirmed on October 21.
  This is not a claim of UK company registration, UK-only hosting or GB-only availability.
- Retention schedule approved on October 21 as an implementation target after the
  requested proposal. See retention-policy.json and POLICY-IMPLEMENTATION.md.
  Production implementation, effective publication and deletion of existing data
  have not been completed or authorized by that decision alone.
- Initial service eligibility: users aged 18 or older, explicitly confirmed by the
  operator on October 21. Enforcement still needs implementation and verification.
- Support: support@awiki.ai and https://matchall.net/support.
- All platform-available regions; the package sets countries to an empty list.
- Matching is free; participants arrange transactions outside the platform.
- An administrator will operate the submission portal. Do not access an unrelated
  person's logged-in account or create a duplicate submission to bypass access.

Still required before the corresponding step:

- Implement and verify the confirmed 18+ eligibility policy across the website,
  OAuth and MCP entry points. A policy decision alone is not deployed enforcement.
- Implement and verify the approved retention/deletion schedule across accounts,
  intentions, contacts, audit, logs and backups; confirm any specific exceptions.
  The current daily backup script has no automatic cleanup. Closing an intent
  is not account deletion.
- Hosting and relevant processing locations, and actual processor arrangements.
  Production configuration identifies DeepSeek chat and Aliyun Bailian embeddings;
  a configuration label of "local" is not proof of local data processing.
- Actual reviewer mailbox delivery and sign-in verification. The current portal
  supports email codes and its designated account and synthetic samples are
  pre-provisioned. The reviewer receives their own code; no owner mailbox is needed.
- Review of broader matching use cases against the current commerce rules.
  Free matching and off-platform transactions do not establish compliance.
- The administrator's correct organization/project and existing submission,
  portal-issued domain challenge, OAuth connection and scans, verified developer
  identity, policy attestations and final submission.

The user explicitly authorized policy-page deployment on October 21. The public
privacy and terms pages are now live; policy-drafts/ retains superseded drafts. The hosted video is a real
October 22 development walkthrough; its existence does not mark the eight
package-specific ChatGPT cases as passed. See ADMIN-HANDOFF.md for sequencing.

Portal evidence supplied on October 21:

- The screenshot shows 0.1.3 Draft and the match-service skill check passed.
- MCP details cannot be saved because its URL is already used by another app in
  the same organization. The owning app is not yet identified; see MCP-URL-CONFLICT.md.

Latest October 22 evidence supersedes the earlier portal blockers: MCP shows
Configured/account connected. The portal-designated reviewer email is provisioned
with synthetic data. Actual mailbox login and final-package case execution remain
unverified; the administrator still handles secure fields and submission.

October 22 recording update: eight prompts were executed through a development
MCP connection and the new edited MP4 is hosted. Standard fresh-account OAuth
scope compatibility and complete-plugin acceptance remain open; see
DEVELOPMENT-REHEARSAL-20261022.md.
