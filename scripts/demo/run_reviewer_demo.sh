#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-reviewer-demo-output}"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/full-manager-reviewer.XXXXXX")"

cleanup() {
  rm -rf "$TMP_DIR"
  rm -rf "$ROOT/demo-console/node_modules" "$ROOT/demo-console/public" "$ROOT/demo-console/dist"
}
trap cleanup EXIT INT TERM

for tool in git python3 node npm; do
  command -v "$tool" >/dev/null || { echo "missing required tool: $tool" >&2; exit 2; }
done

PYTHON_VERSION="$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
NODE_VERSION="$(node --version)"
NPM_VERSION="$(npm --version)"
printf 'python=%s\nnode=%s\nnpm=%s\n' "$PYTHON_VERSION" "$NODE_VERSION" "$NPM_VERSION" > "$OUT_DIR/tool-versions.txt"

python3 -m venv "$TMP_DIR/venv"
"$TMP_DIR/venv/bin/python" -m pip install --disable-pip-version-check --no-input -e platform/app
"$TMP_DIR/venv/bin/python" -m pip freeze | LC_ALL=C sort > "$OUT_DIR/python-environment.txt"
sha256sum "$OUT_DIR/python-environment.txt" > "$OUT_DIR/python-environment.sha256"

npm --prefix demo-console install --ignore-scripts --no-audit --no-fund --package-lock=false
npm --prefix demo-console run check
npm --prefix demo-console run build
npm --prefix demo-console ls --all --json > "$OUT_DIR/npm-tree.json" || true
sha256sum "$OUT_DIR/npm-tree.json" > "$OUT_DIR/npm-tree.sha256"

mkdir -p "$OUT_DIR/console"
cp -R demo-console/dist/. "$OUT_DIR/console/"

export REVIEWER_SOURCE_COMMIT="$(git rev-parse HEAD)"
"$TMP_DIR/venv/bin/python" scripts/demo/reviewer_demo.py \
  --manifest evidence/receipts/convergence/public-inputs.json \
  --console-dist demo-console/dist \
  --output-dir "$OUT_DIR"

sha256sum "$OUT_DIR/reviewer-demo-receipt.json" > "$OUT_DIR/reviewer-demo-receipt.sha256"
printf 'PASS_BOUNDED\n' > "$OUT_DIR/VERDICT"

echo "reviewer demo complete: $OUT_DIR"
