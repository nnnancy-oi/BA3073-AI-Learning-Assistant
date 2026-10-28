# BNBU student email registration — 2026-10-25

## Problem and scope

The user could not register with their institutional email. They confirmed the
email domain is `mail.bnbu.edu.cn`; the supplied validator accepted only
`bnbu.edu.cn`. Both registration and login shared this validator.

## Changes

- Added the exact `mail.bnbu.edu.cn` suffix alongside `bnbu.edu.cn` in
  `backend/core/weak_auth.py`.
- Expanded authentication API tests to cover registration/login for both domains,
  mixed case and surrounding whitespace, rejection of unrelated and lookalike
  domains on both endpoints, and existing bearer-token rejection checks.
- Updated the auth contract, ADR 010, product specification, and the factual
  auth-domain summary in `AGENTS.md`.
- Existing role values, API shapes, password hashing, sessions, key storage,
  dependencies, and persisted application data were retained.

## Verification

- In a separate container with networking disabled, mounted only source/test
  files read-only and ran:
  `python -m pytest -p no:cacheprovider backend/tests/test_auth_sqlite.py backend/tests/test_model_settings.py backend/tests/test_user_model_keys.py -q`.
  Result: **23 passed in 0.81s**. Production data was not mounted.
- Rebuilt the image and ran Compose with `up --build -d --wait --wait-timeout 90`.
  All dependency layers were reused; the replacement backend became healthy.
- Checked the validator inside the running replacement container: both exact
  BNBU domains were accepted and lookalike/other subdomains were rejected.
- `/health` returned `{"status":"ok"}`.
- `scripts/check-local-ui.sh` passed with HTTP 200 at
  2026-10-25 21:56:23 +0800; `local-ui-check.txt` was refreshed.
- `git diff --check` passed.

## User follow-up

Refresh the local browser page and retry registration with the user's own
`@mail.bnbu.edu.cn` address. Model-key setup and a real artifact generation are
still pending. No real password, API key, or session token was read or recorded.
