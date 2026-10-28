# BA3073 report-generation instruction revision

Date: 2026-10-26 (Asia/Shanghai)

## Scope and changes

- Revised `backend/pipelines/essay_html.py::build_essay_html_prompt` for the README Task 1 requirement. The prompt now covers Tasks 1-3, actual architecture, explanations, deployment evidence, test outcomes, troubleshooting, security/cost factors, and justified improvements.
- Added instructions to distinguish completed work from plans, mark missing evidence, use genuine screenshots, and exclude secrets and invented references/results.
- Set a complete-report target of no more than 20 A4 pages, with readable print typography, wrapping, and practical page-break guidance. Short test requests and unrelated essays retain their requested scope.
- Updated `docs/SPEC.md` to record this report-generation goal. No HTTP, storage, artifact-filesystem, or auth contract changed in this task; no new dependency was added.

## Verification

- Isolated test container: `docker run --rm --network none` with `backend/` and `pytest.ini` mounted read-only, `TESTING=1`, using the existing local image; `python -m pytest -p no:cacheprovider backend/tests/test_essay_pipeline.py -q`: **3 passed in 0.09s**. Tests cover source/PDF success, retained HTML on conversion failure, and provider failure. Model and converter are mocked; this is not a new live Qwen quality test.
- `git diff --check`: passed.
- `docker compose --progress plain -p ai-learning-assistant up --build -d --wait --wait-timeout 90`: built successfully, backend healthy.
- Runtime and host source SHA-256 match: `b71394081ce09b5cd734471eb921dc12428476b44d1965cb20055b815df61edc`.
- `bash scripts/check-local-ui.sh`: HTTP 200, PASS at 2026-10-26T00:58:23+0800; refreshed root `local-ui-check.txt`.
- `GET /health`: `{"status":"ok"}`.

## Existing live smoke evidence

Before this prompt revision, the user successfully generated the local smoke report. Its original HTML, unchanged PDF, address-bar screenshot, and previous local check were copied to the parent folder `证据/Task1_本地运行/`, outside the source repository. The 2-page PDF was rendered and both pages inspected: Chinese characters readable, no clipped content. Preview PNGs were moved out of the source repository into the same evidence folder's `预览/` directory.

## Remaining work and limitations

- The prompt guides model behavior; it does not enforce PDF page count in code. Inspect and count the final report after real screenshots are included.
- Complete Task 2 ACR/ECS deployment and Task 3 domain/TLS/independent access control before using the deployed assistant to produce the final assignment report.
- The user confirmed they already have an ECS instance; next obtain its actual region, OS, instance configuration, and public IP through the console. No cloud resource was changed in this task.
- Earlier school-email compatibility changes and their QA records remain uncommitted alongside this task. Nothing has been pushed to a personal GitHub repository yet.
