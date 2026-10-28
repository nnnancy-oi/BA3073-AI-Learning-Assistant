# ECS startup verification

Date: 2026-10-26 (Asia/Shanghai)

## Verified from user-provided terminal screenshots

- ECS image list contains the intended repository/tag and manifest digest `sha256:1f80d6842dfca002b0b5542ea6b88ae8be2c20f25f85c0721918720fe6966dfd`.
- User executed the provided Compose startup command in Workbench Shell.
- Project `ai-learning-assistant`: network created and backend container Healthy after about 11 seconds.
- Published binding: `127.0.0.1:14242->14242/tcp`.
- Server-side health response: `{"status":"ok"}`.
- Server-side UI HTTP status: 200.
- Persistent data/workspace directories are under the server project folder `/root/个人_Cloud/AI_Learning_Assistant/`.
- The digest-pinned Compose template contains only non-secret model endpoint defaults. Personal Qwen keys are not included in the image/template.

## Evidence and next steps

The unchanged startup screenshot is retained outside the source repository at `../证据/Task2_云端部署/ECS_容器健康与内部网页检查成功.png`. Cloud deployment templates and pasteable commands are in the parent folder `云端部署/`; syntax and Compose format checks passed.

Public-IP browser access is not yet verified. First inspect the instance security group and restrict inbound TCP 14242 to the current client public IPv4 /32, then change the host binding for the direct-access test. Still pending: browser screenshot with address bar, actual cloud model/generation test, `ecs-docker-check.txt`, and Task 3 domain/HTTPS/independent access control. The private client-IP measurement is in the parent progress record, not required in this source QA record.

## External direct-access diagnostic

After the source-restricted security-group rule and host-binding update, Mac direct requests returned HTTP 200 for the public-IP health endpoint and UI. Downloaded main JS and CSS bytes exactly match the supplied local static assets. The user's Safari screenshot is still blank. The same UI request through the configured Clash HTTP proxy timed out after 12 seconds with no response, and read-only macOS proxy inspection confirms HTTP/HTTPS/SOCKS system proxy use with no ECS-IP bypass entry. These observations identify the proxy route as the next issue to address; they do not yet establish successful Safari rendering. A system-proxy bypass for this ECS IP is pending user configuration. The evidence folder contains detailed diagnostics and the original screenshot. No application source change is indicated by these checks.

## Safari rendering verified

After the user added this ECS IP to the system-proxy bypass list, the user's 2026-10-26 19:33 screenshot shows the actual cloud application's login/registration page rendered in Safari. This resolves the blank-page proxy-route blocker. The original screenshot is preserved outside Git under the evidence folder. Cloud application registration/login, final workbench screenshot with full address, required ECS check-file generation/download, and Task 3 remain pending.

## Authenticated workbench evidence

The user's 19:53 screenshots confirm an authenticated cloud workbench and the full public URL `47.99.44.61:14242/ui/`. Originals are retained under the evidence folder as `ECS_登录后工作台.png` and `ECS_完整公网URL确认.png`. The workbench is idle; actual cloud model/generation verification remains pending. The required ECS check command is ready, but the original check file still needs server execution and retrieval. A fresh direct request to the public health endpoint returned `{"status":"ok"}`.

## Required ECS check: public self-request timeout

The user ran the README-based required check on ECS at 20:03:45+0800. Screenshot evidence confirms Docker 29.8.0, a healthy backend, and `0.0.0.0:14242->14242/tcp`. However, ECS's request to its own public UI URL timed out after 5 seconds (curl 28, HTTP 000), producing an actual FAIL in `ecs-docker-check.txt`. Preserve that original result. A subsequent direct Mac request to public `/health` returned HTTP 200 and status=ok; browser login already succeeded. The security-group source restriction versus the ECS self-request is a hypothesis to test, not a confirmed platform NAT limitation. No security-group change or fabricated PASS has been made. Next diagnostic checks ECS loopback UI and actual outbound public IPv4; server-side files still require retrieval.

## ECS source diagnostic confirmed

The user's 21:08 screenshot shows loopback UI HTTP 200 and actual outbound IPv4 matching the ECS public IP. The current ingress source allowance is the student's Mac public /32, so a controlled experiment is now planned: temporarily allow TCP 14242 only from the ECS own public /32, using the description `TEMP-ECS-SELF-CHECK`, and repeat the same public URL check. This rule has not yet been added and the cause is not yet proven. Remove the temporary rule after testing/recording; final 14242 access must remain limited to the student's client IP. Preserve the original FAIL check file before any rerun. The unchanged diagnostic screenshot is saved outside Git in the evidence folder.

## Narrow self-source experiment succeeded

After the user added the planned temporary ingress allowance only for the ECS own /32, the same public UI request returned HTTP 200 (21:20 screenshot). This supports the source-allowlist diagnosis. Next: back up the original FAIL, rerun the unchanged required network test to capture its actual result, then immediately remove `TEMP-ECS-SELF-CHECK` and verify the final client-only rule. The exception is currently active and removal has not been confirmed. Any report must state the temporary self-source test condition and subsequent withdrawal; do not describe its PASS as a check performed under a client-only ingress rule. The real rerun file and originals remain to be retrieved.

## Required check passed; temporary allowance removed

The user's final screenshots confirm the actual required check at 21:24:09+0800: healthy container, published 0.0.0.0:14242, HTTP 200, and Website URL check: PASS. The rerun command backed up the earlier FAIL before producing this new result. A separate 21:24:53 security-group screenshot confirms removal of TEMP-ECS-SELF-CHECK; final TCP 14242 ingress is restricted to the student's client /32. The PASS was captured while the temporary ECS own /32 exception existed; reports must disclose that condition and its removal. Do not expect the ECS public self-request to pass again under the final client-only rule. The original check text and failure backup remain on ECS, pending retrieval; screenshot transcription is not a substitute for the original file. No application code or contract changed in this verification step.

## Original check file retrieved (2026-10-27)

The Workbench-downloaded original ecs-docker-check.txt was found in Downloads, read and checked against the successful screenshot, then copied unchanged to ../证据/Task2_云端部署/ecs-docker-check.txt. Source and archive bytes match; SHA-256: `63a3cf92d268e9f35965e1d19319b3d916c7f4bf8f4a0899201ecb7178f5661e`. It records 2026-10-26T21:24:09+0800, HTTP 200 and PASS. The temporary test condition documented above still applies. Earlier FAIL and diagnostic text backups remain on the server.
