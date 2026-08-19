#!/usr/bin/env bash
set -euo pipefail

: "${M6_LLAMA_CPP_COMMIT:?M6_LLAMA_CPP_COMMIT must be an exact 40-hex Git SHA}"
: "${M6_MODEL_URL:?M6_MODEL_URL must be the exact HTTPS model artifact URL}"
: "${M6_MODEL_SHA256:?M6_MODEL_SHA256 must be the exact model SHA-256}"
: "${M6_MODEL_LICENSE_ID:?M6_MODEL_LICENSE_ID must be the admitted model license identifier}"

exec python3 scripts/handoff/run_local_model.py \
  --llama-commit "$M6_LLAMA_CPP_COMMIT" \
  --model-url "$M6_MODEL_URL" \
  --model-sha256 "$M6_MODEL_SHA256" \
  --model-license-id "$M6_MODEL_LICENSE_ID" \
  "$@"
