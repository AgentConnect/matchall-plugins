# Matchall plugin repository

- This is a Python packaging repository, separate from the Rust matching backend.
- Keep business instructions and assets in `shared/`; do not duplicate them per host.
- Preserve existing plugin IDs, OAuth endpoint, versions, consent rules and review evidence.
- Register each adapter in `platforms.json`. Generated directories are not source files.
- Before a PR, run `python -m unittest discover -s tests -v`,
  `python scripts/validate.py` and `python scripts/package.py` in the development environment.
- Tests must cover actual packaging, consent-rule preservation, platform isolation or failure paths.
- New adapters start with unverified host status; never copy another host's passing evidence.
- Source commits/PRs do not authorize releases, marketplace submission, installation or deployment.
- Keep PR titles and descriptions in English. Use `Feature/`, `BugFix/` or `Docs/` branches.
