#!/usr/bin/env bash
set -euo pipefail

VERSION="${SYFT_VERSION:-1.50.0}"
DEST="${1:-$PWD/.tools}"
ARCHIVE="syft_${VERSION}_linux_amd64.tar.gz"
BASE="https://github.com/anchore/syft/releases/download/v${VERSION}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$DEST"
curl --fail --silent --show-error --location "$BASE/$ARCHIVE" -o "$TMP/$ARCHIVE"
curl --fail --silent --show-error --location "$BASE/syft_${VERSION}_checksums.txt" -o "$TMP/checksums.txt"
(
  cd "$TMP"
  grep "  ${ARCHIVE}$" checksums.txt | sha256sum --check --strict
)
tar -xzf "$TMP/$ARCHIVE" -C "$DEST" syft
"$DEST/syft" version
