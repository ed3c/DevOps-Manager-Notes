#!/usr/bin/env bash
set -euo pipefail

: "${M7_ARGO_KIND_NODE_IMAGE:?M7_ARGO_KIND_NODE_IMAGE must be exact name@sha256:<64 hex>}"
: "${M7_ARGO_TARGET_REVISION:?M7_ARGO_TARGET_REVISION must be exact 40-hex Git SHA}"
: "${M7_ARGO_CD_MANIFEST_URL:?M7_ARGO_CD_MANIFEST_URL is required}"
: "${M7_ARGO_CD_MANIFEST_SHA256:?M7_ARGO_CD_MANIFEST_SHA256 is required}"
: "${M7_ARGO_ROLLOUTS_MANIFEST_URL:?M7_ARGO_ROLLOUTS_MANIFEST_URL is required}"
: "${M7_ARGO_ROLLOUTS_MANIFEST_SHA256:?M7_ARGO_ROLLOUTS_MANIFEST_SHA256 is required}"

exec python3 scripts/handoff/run_argo_ephemeral_kind.py \
  --kind-node-image "$M7_ARGO_KIND_NODE_IMAGE" \
  --target-revision "$M7_ARGO_TARGET_REVISION" \
  --argocd-manifest-url "$M7_ARGO_CD_MANIFEST_URL" \
  --argocd-manifest-sha256 "$M7_ARGO_CD_MANIFEST_SHA256" \
  --rollouts-manifest-url "$M7_ARGO_ROLLOUTS_MANIFEST_URL" \
  --rollouts-manifest-sha256 "$M7_ARGO_ROLLOUTS_MANIFEST_SHA256" \
  "$@"
