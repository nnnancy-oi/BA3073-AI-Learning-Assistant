# ACR personal-edition manifest compatibility

Date: 2026-10-26 (Asia/Shanghai)

## Observed failure

After the proxy-bypass retry, authentication and layer transfer progressed. The registry rejected a manifest with `unknown manifest class for application/vnd.oci.empty.v1+json`. This media type matches the OCI artifact attestation config used by recent BuildKit; the first local image descriptor was an OCI index including an attestation. This supports an attestation-format compatibility diagnosis for this registry, rather than a failed application build.

## Fix and verification

- Reused the existing Dockerfile and build cache, exporting `ai-learning-assistant-backend:ecs-amd64-acr` with `--platform linux/amd64 --provenance=false --sbom=false --load`.
- Build succeeded with all application/dependency layers cached; no Dockerfile, dependency, or application source edits.
- New top-level descriptor: `application/vnd.oci.image.manifest.v1+json`, digest `sha256:1f80d6842dfca002b0b5542ea6b88ae8be2c20f25f85c0721918720fe6966dfd`.
- Image config digest `sha256:8a9da8f2cc6e23779334c10d64dbba7143c3c7bc9f254ac5e105ebdbea08dbc2`.
- Compared Docker image inspection records: RootFS and runtime Config exactly equal between original and compatible images; platform remains linux/amd64. Previous isolated runtime health, UI, and real Chromium PDF checks therefore apply to the unchanged runtime contents.
- Updated the parent-folder upload script SOURCE_IMAGE and public deployment metadata. Script syntax and local preflight checked separately.
- Build log, failed upload log, and unchanged screenshot are retained outside Git under `../证据/Task2_云端部署/`.

## Pending

The user must re-run the local upload script and enter the Registry password privately. Remote push success and ECS pull/run are not yet verified. The source snapshot remains available alongside plain build logs; this deployment export omits build attestations for compatibility.

## Sources

- https://docs.docker.com/build/metadata/attestations/ (OCI empty config descriptor used by artifact attestations)
- https://docs.docker.com/reference/cli/docker/buildx/build/ (--provenance=false and --sbom=false)

## Successful retry

The user subsequently reported success. The actual local push log `acr-push-20261026-015155.log` confirms `Result: PASS`, with remote digest `sha256:1f80d6842dfca002b0b5542ea6b88ae8be2c20f25f85c0721918720fe6966dfd`, size 2951, matching the compatible local manifest. Temporary credential directories remaining: 0. ECS pull and runtime verification remain pending.
