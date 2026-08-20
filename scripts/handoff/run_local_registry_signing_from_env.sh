#!/usr/bin/env bash
set -euo pipefail

: "${M6_REGISTRY_IMAGE:?M6_REGISTRY_IMAGE must be exact name@sha256:<64 hex>}"
: "${M6_COSIGN_BIN:?M6_COSIGN_BIN must be the admitted cosign binary path}"
: "${M6_COSIGN_SHA256:?M6_COSIGN_SHA256 must be the exact cosign binary SHA-256}"

exec python3 scripts/handoff/run_local_registry_signing.py \
  --registry-image "$M6_REGISTRY_IMAGE" \
  --cosign-bin "$M6_COSIGN_BIN" \
  --cosign-sha256 "$M6_COSIGN_SHA256" \
  "$@"
