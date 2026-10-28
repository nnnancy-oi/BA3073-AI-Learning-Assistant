# Linux amd64 deployment image

Date: 2026-10-26 (Asia/Shanghai)

## ECS preflight (user-provided console/terminal screenshots)

- Region: China East 1 (Hangzhou); Ubuntu 22.04, x86_64, 2 vCPU / 2 GiB.
- Available memory about 1.3 GiB, no swap; root disk 40 GB with about 34 GB free.
- Docker 29.8.0; Compose v5.5.1; no existing containers listed.
- Screenshot retained unchanged outside the source repository at `../证据/Task2_云端部署/ECS_架构与Docker检查.png`.

## Build and verification

- Built existing Dockerfile with `docker buildx build --builder desktop-linux --platform linux/amd64 --load --tag ai-learning-assistant-backend:ecs-amd64 --progress plain .` through the configured local proxy.
- Build succeeded; image inspection returned `linux/amd64` and `sha256:7ac3a6343aa0130c2f69f521a3736b635ba5c7d4cd949e8994c1e9fb94c5b09d`.
- Existing local arm64 image tag was retained. No Dockerfile or dependency file changed.
- Used a separate temporary `--rm --platform linux/amd64 --network none` container, without host data/workspace mounts or API credentials.
- Architecture: x86_64. FastAPI TestClient health: 200 / status=ok. UI: 200. Actual Playwright Chromium HTML-to-PDF conversion: valid PDF signature, 17,594 bytes.
- Expected missing-model-key warning appeared; no Qwen API request was made.
- Build and smoke logs saved outside the source repository under `../证据/Task2_云端部署/`.

## Pending

The user is at the ACR instance list with a personal-edition creation card. Create/open the personal instance, then create a namespace and private repository; obtain actual registry address and login name. Registry password must be entered by the user. Push, ECS pull/deployment, cloud evidence and domain/HTTPS remain pending. A local emulated architecture smoke does not replace verification on the actual ECS.
