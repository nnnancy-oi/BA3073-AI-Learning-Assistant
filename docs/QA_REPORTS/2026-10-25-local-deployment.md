# Local deployment verification — 2026-10-25

Scope: initial local Docker deployment for BA3073 Task 1. Cloud deployment and final report are not completed by this check.

## Environment

- Source revision: `242afd54ca88fb3eba2cb2f6099164eb86b6317e`
- Host: Apple Silicon / arm64, macOS 15.7.4.
- Docker Engine: 29.8.2; Docker Compose: v5.6.0.
- Compose project: `ai-learning-assistant`.
- Project directory: `/Users/mac/Desktop/个人_Cloud/AI_Learning_Assistant`.

## Local configuration

- Created a Git-ignored `.env` containing the user-provided model Base URL and `AILA_BACKEND_PORT=127.0.0.1:14242`.
- No API key was requested in chat, read, or written by the agent.
- Application source code and Dockerfile were unchanged during this deployment.
- Runtime data and generated artifacts use the supplied `data/` and `workspace/` bind mounts inside this project.

## Issues and resolution

1. The original repository download was interrupted. Confirmed that no Git process remained, renamed the stale shallow lock to preserve it, fetched the upstream main branch, and checked out the source successfully.
2. Docker Hub authentication timed out on the direct connection. The user configured Docker Desktop to use their existing local HTTP proxy. A request through that proxy to the official Docker authentication endpoint returned HTTP 200. Supplying the same proxy explicitly to the build command resolved the authentication timeout.
3. The first Playwright CDN timed out while downloading Chromium and the headless shell. Playwright automatically retried through its alternate CDN and installed both successfully. No Dockerfile workaround was required.

## Verification results

- `docker compose -p ai-learning-assistant config --quiet`: passed.
- `docker compose --progress plain -p ai-learning-assistant up --build -d`: exited successfully.
- `docker compose -p ai-learning-assistant ps`: backend running and healthy; mapping `127.0.0.1:14242->14242/tcp`.
- `GET http://127.0.0.1:14242/health`: returned `{"status":"ok"}`.
- `bash scripts/check-local-ui.sh --open`: passed; UI HTTP 200; generated `local-ui-check.txt` at 2026-10-25 21:44:40 +0800.
- Default-browser launch request accepted. Actual browser rendering, account registration, model connectivity, and artifact generation remain to be confirmed with the user.

## Remaining assignment work

- Register an application account, configure the personal model key, and test a real generation.
- Capture the successful local interface with the browser address bar visible.
- Revise the report-generation instructions in `backend/pipelines/essay_html.py`.
- Complete ECS/ACR and HTTPS-domain deployment, collect their evidence, and generate the final assignment report.

No authentication passwords, API keys, session tokens, or encryption keys are included in this record.
