#!/usr/bin/env bash
set -euo pipefail

# Download and pin @openuidev/browser-bundle for reproducible air-gapped hosting
VERSION="${OPENUI_BROWSER_BUNDLE_VERSION:-0.1.4}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/openui-assets/dist"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cd "$TMP_DIR"
npm pack "@openuidev/browser-bundle@${VERSION}"
tar -xzf openuidev-browser-bundle-*.tgz

mkdir -p "$DIST_DIR"
cp package/dist/openui-bundle.min.js "$DIST_DIR/"
cp package/dist/openui-styles.css "$DIST_DIR/"

echo "OpenUI bundle v${VERSION} extracted to ${DIST_DIR}"
