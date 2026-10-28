# BA3073 coursework source

This repository contains the complete teaching project derived from https://github.com/bnbu-busa-projects/AI_Learning_Assistant with coursework modifications and deployment documentation.

## Changes

- backend/pipelines/essay_html.py: evidence-led report instructions covering Tasks1-3, technical explanation, real evidence, secret exclusion and the20-page limit.
- backend/core/weak_auth.py with matching tests/contracts: accept exact mail.bnbu.edu.cn addresses alongside bnbu.edu.cn, rejecting unrelated/lookalike domains.
- Prior focused validation:23 auth/model API tests and3 essay pipeline tests passed. Real local and cloud HTML/PDF generation was completed; mocked unit checks are distinguished in QA records.
- deploy/hongkong/: actual Nginx/auth-sidecar templates with signing key and bcrypt hashes redacted.

Follow README.md for build/run instructions. The report and original local-ui-check.txt and ecs-docker-check.txt are submitted separately, outside this source repository. No personal cover information, environment files, API keys, passwords, auth hashes, session cookies, private keys, databases, generated runtime workspaces or installed dependencies are included.
