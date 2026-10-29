# Matchall for ChatGPT

> Source is maintained in [Matchall Plugins](https://github.com/AgentConnect/matchall-plugins).
> This platform directory is an input to the build, not an installable plugin root.
> Build from the monorepo root with `python scripts/package.py --platform chatgpt`.
> Use the generated `dist/matchall-chatgpt/` directory or preparation ZIP.
> Dated review reports below describe prior evidence, not acceptance of this new build.

Public source preparation for the Matchall ChatGPT plugin. **Not submitted to or
approved by the ChatGPT plugin directory.** The manifest version identifies this
source package; no GitHub release or marketplace version has been published.

## Package and installation path

The generated plugin uses Agent Plugins 1.0: root `plugin.json`, `mcp.json`, and
`skills/match-service/SKILL.md`. The manifest uses the `matchall-chatgpt`
name and includes OpenAI listing metadata plus five positive and three
negative review cases.

Build the ZIP using the commands below. An authorized developer can later upload
it as a draft through the OpenAI plugin submission portal, configure the remote
OAuth connection, and run the review cases. A GitHub upload does not install the
plugin into ChatGPT or replace an existing private installation. This package is
**not submission-ready**; missing listing and review items are tracked below.

## What Matchall does

Draft needs and offers in natural language, activate them after approval, inspect
matches, and exchange private contact details only with mutual consent. Pause or
close needs when appropriate. Match scores do not guarantee transactions;
Matchall does not place orders or process payments.

## Authorization and data

The remote MCP endpoint for this candidate is
`https://matchall.net/amatch/v2`. Version 0.1.6 restores the existing app's
original URL after the portal rejected 0.1.5's URL change. The deployed
`/mcp/chatgpt` alias remains available but is not used by this package.
See [the binding conflict handoff](docs/MCP-URL-CONFLICT.md) and
[endpoint validation history](docs/CHATGPT-ENDPOINT.md).
The latest user screenshot shows the portal account connected and MCP Configured.
A new tool scan after the deployed annotation fix and final-package acceptance
remain to be confirmed.
Use the host's OAuth connection UI. Discovery advertises PKCE S256, dynamic
client registration, and `intent:read` / `intent:write` scopes. Never put tokens,
passwords, verification codes, or private contact details in this repository.
Do not configure shared secret headers as an OAuth workaround.

Email binding is optional and helps with account recovery and notifications.
Private contact details are entered separately from business text and login
email. Without email, use manual checks or a host-supported scheduled task.
A schedule is not created merely by installing this plugin.
Business text is processed by the hosted Matchall service and its configured
model providers. This repository is the client plugin package, not the backend.

## Example prompts

- “Draft a need for five standing desks in Singapore. Show me before activating.”
- “Show current matches and explain which product fits have been verified.”
- “Ask this matched supplier to exchange contact details after showing me mine.”
- “Pause my standing-desk need; keep it for later.”

## Development

Run from the **monorepo root**, after cloning Matchall Plugins:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py --platform chatgpt
python scripts/package.py --platform chatgpt
```

The validator uses pinned Agent Plugins 1.0.0 schemas with recorded source URLs
and hashes, so package validation does not depend on a live schema download.
It checks package structure, referenced assets, contact workflow,
review case inventory, and absence of embedded credentials. ZIP generation is
local only, uses an explicit file allowlist, and inspects the generated archive.
Neither script installs a plugin, invokes matching tools, deploys the service,
or submits a marketplace application. CI only validates and packages locally.
See the [checkbox checklist](docs/SUBMISSION-CHECKLIST.md),
[reviewer guide](docs/REVIEWER-GUIDE.md) and [readiness](docs/READINESS.md) for the
remaining marketplace work. Historical drafts in `docs/policy-drafts/` are superseded by the public pages.
Archive-readable copies are in `docs/published-policies/`. Page availability is
separate from validation of the remaining operational and legal arrangements.

## Support and license

Use this repository's Issues for public package bugs. Never post credentials,
private contact details, or account recovery information in issues. For account, privacy and abuse requests use
[Matchall Support](https://matchall.net/support) or support@awiki.ai. Privacy and
terms are published at [Privacy Policy](https://matchall.net/privacy) and
[Terms of Service](https://matchall.net/terms). Their links remain included in 0.1.10.
The privacy notice explicitly discloses pending cleanup and provider-verification
work. See [retention plan](docs/POLICY-IMPLEMENTATION.md).

The [public development walkthrough](https://matchall.net/review/matchall-chatgpt-demo-20261023.html) requires no
sign-in. Its direct MP4 URL is in the manifest; it is not acceptance evidence for
the current package. See [administrator handoff](docs/ADMIN-HANDOFF.md).

[MIT](https://github.com/AgentConnect/matchall-plugins/blob/main/LICENSE) applies to this plugin package. It does not grant access to other
users' data, relicense the hosted backend, or imply permission to impersonate
AWiki, Matchall, OpenAI, Cursor, or xAI. The monochrome logo follows AWiki branding.

## Matchall naming transition

The plugin is now named `matchall-chatgpt` and the MCP connection label is
`matchall`. Its original source repository was
[AgentConnect/matchall-chatgpt](https://github.com/AgentConnect/matchall-chatgpt); current maintenance is in Matchall Plugins.
The MCP endpoint now targets the dedicated Matchall instance. The older
`awiki.info` instance is separate; its accounts are not silently migrated.
The dedicated instance retains its stable OAuth issuer identity and explicitly
configured legacy resource compatibility. Account data and permissions are not
changed by this package update.
This source update does not publish a release or update installed host copies.

The administrator reported a duplicate binding for the original MCP URL. The
owner subsequently authorized deployment of the new endpoint used by 0.1.5.
The portal has now explicitly rejected the URL change in this existing draft.
Version 0.1.6 restores the original URL while retaining policy and demo links;
the later screenshot shows MCP Configured and account connected. The earlier
binding error is retained as history, not asserted as a current blocker. Do not
retry 0.1.5 on this draft or delete the app to try to free its URL.


## Review preparation 0.1.10

The current portal supports email-code login. Dedicated synthetic reviewer data
has been provisioned; actual reviewer mailbox delivery and sign-in are unverified.
The updated five positive cases run with one reviewer account and a pre-seeded
seller; P4 cancels the buyer's pending request instead of requiring seller login.
Each run creates a fresh P1 intention. Three negative cases and the original MCP
URL are retained. All eight cases were executed through a separate development
MCP connection on October 22; the updated recording is public. Complete-package
acceptance remains unverified, and a standard fresh-account OAuth scope issue
requires repair and retesting. See [rehearsal evidence](docs/DEVELOPMENT-REHEARSAL-20261022.md).
Credentials and exact sign-in instructions belong only in secure portal fields.

The current demonstration includes English AI narration added on October 23 and
optional English captions. The recorded ChatGPT video is unchanged.

The listing now uses Business & Operations and describes the buyer/seller matching workflow with a concrete used-computer example. See [category rationale](docs/LISTING-CATEGORY.md); portal acceptance is unverified.
