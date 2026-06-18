#!/bin/zsh
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOOLKIT_DIR="$ROOT_DIR/.venv/lib/python3.9/site-packages/swmm/toolkit"

if [ ! -d "$TOOLKIT_DIR" ]; then
  echo "PySWMM toolkit directory not found: $TOOLKIT_DIR"
  exit 0
fi

xattr -cr "$TOOLKIT_DIR" 2>/dev/null || true
find "$TOOLKIT_DIR" \( -name '*.so' -o -name '*.dylib' \) -print0 | while IFS= read -r -d '' binary; do
  codesign --force --sign - "$binary" >/dev/null 2>&1 || true
done

echo "Repaired PySWMM macOS binary signatures."
