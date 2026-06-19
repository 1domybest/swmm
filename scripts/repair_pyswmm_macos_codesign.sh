#!/bin/zsh
set -e

TOOLKIT_DIR="$(python3 - <<'PY'
import importlib.util

spec = importlib.util.find_spec("swmm.toolkit")
if spec and spec.submodule_search_locations:
    print(spec.submodule_search_locations[0])
PY
)"

if [ -z "$TOOLKIT_DIR" ] || [ ! -d "$TOOLKIT_DIR" ]; then
  echo "PySWMM toolkit directory not found: $TOOLKIT_DIR"
  exit 0
fi

xattr -cr "$TOOLKIT_DIR" 2>/dev/null || true
find "$TOOLKIT_DIR" \( -name '*.so' -o -name '*.dylib' \) -print0 | while IFS= read -r -d '' binary; do
  codesign --force --sign - "$binary" >/dev/null 2>&1 || true
done

echo "Repaired PySWMM macOS binary signatures."
