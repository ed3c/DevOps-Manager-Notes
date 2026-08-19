#!/usr/bin/env bash
set -euo pipefail

: "${M6_ARGO_CLUSTER_CONTEXT:?M6_ARGO_CLUSTER_CONTEXT must be kind-manager-demo-*}"
: "${M6_ARGO_TARGET_REVISION:?M6_ARGO_TARGET_REVISION must be an exact 40-hex Git SHA}"
: "${M6_ARGO_CD_MANIFEST_URL:?M6_ARGO_CD_MANIFEST_URL is required}"
: "${M6_ARGO_CD_MANIFEST_SHA256:?M6_ARGO_CD_MANIFEST_SHA256 is required}"
: "${M6_ARGO_ROLLOUTS_MANIFEST_URL:?M6_ARGO_ROLLOUTS_MANIFEST_URL is required}"
: "${M6_ARGO_ROLLOUTS_MANIFEST_SHA256:?M6_ARGO_ROLLOUTS_MANIFEST_SHA256 is required}"

exec python3 scripts/handoff/run_argo_control_plane.py \
  --cluster-context "$M6_ARGO_CLUSTER_CONTEXT" \
  --target-revision "$M6_ARGO_TARGET_REVISION" \
  --argocd-manifest-url "$M6_ARGO_CD_MANIFEST_URL" \
  --argocd-manifest-sha256 "$M6_ARGO_CD_MANIFEST_SHA256" \
  --rollouts-manifest-url "$M6_ARGO_ROLLOUTS_MANIFEST_URL" \
  --rollouts-manifest-sha256 "$M6_ARGO_ROLLOUTS_MANIFEST_SHA256" \
  "$@"
