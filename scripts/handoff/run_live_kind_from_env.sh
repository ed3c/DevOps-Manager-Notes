#!/usr/bin/env bash
set -euo pipefail

: "${M5_KIND_NODE_IMAGE:?M5_KIND_NODE_IMAGE must be an exact kindest/node name@sha256 digest}"

if [[ ! "$M5_KIND_NODE_IMAGE" =~ ^[^[:space:]]+@sha256:[0-9a-f]{64}$ ]]; then
  echo "M5_KIND_NODE_IMAGE must match name@sha256:<64 lowercase hex>" >&2
  exit 2
fi

exec python3 scripts/handoff/run_live_kind_smoke.py \
  --kind-node-image "$M5_KIND_NODE_IMAGE" \
  "$@"
