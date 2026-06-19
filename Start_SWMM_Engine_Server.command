#!/bin/zsh
set -u

cd "$(dirname "$0")" || exit 1

HOST="${SWMM_ENGINE_HOST:-127.0.0.1}"
PORT="${SWMM_ENGINE_PORT:-8765}"
MODE="${SWMM_ENGINE_MODE:-react}"
HEALTH_URL="http://${HOST}:${PORT}/health"
PYTHON_BIN="${SWMM_PYTHON_BIN:-}"

python_has_pyswmm() {
  "$1" -c "import pyswmm" >/dev/null 2>&1
}

python_has_react_deps() {
  "$1" -c "import fastapi, uvicorn, pyswmm" >/dev/null 2>&1
}

pick_python() {
  local candidate
  local pyenv_root="${PYENV_ROOT:-$HOME/.pyenv}"
  local candidates=()

  if [ -n "$PYTHON_BIN" ]; then
    candidates+=("$PYTHON_BIN")
  fi
  candidates+=(".venv/bin/python")
  if [ -d "$pyenv_root/versions" ]; then
    candidates+=("$pyenv_root"/versions/*/bin/python3(N))
  fi
  candidates+=("python3")

  for candidate in "${candidates[@]}"; do
    if ! command -v "$candidate" >/dev/null 2>&1 && [ ! -x "$candidate" ]; then
      continue
    fi

    if [ "$MODE" = "legacy" ]; then
      if python_has_pyswmm "$candidate"; then
        PYTHON_BIN="$candidate"
        return 0
      fi
      continue
    fi

    if python_has_react_deps "$candidate"; then
      PYTHON_BIN="$candidate"
      return 0
    fi
  done

  return 1
}

if ! pick_python; then
  echo "No Python runtime with required SWMM server dependencies was found."
  echo "Install dependencies with one of these commands:"
  echo "  python3 -m pip install -r requirements.txt"
  echo "  .venv/bin/python -m pip install -r requirements.txt"
  exit 1
fi

echo "Using Python: ${PYTHON_BIN}"

EXISTING_PIDS="$(lsof -tiTCP:${PORT} -sTCP:LISTEN 2>/dev/null || true)"
if [ -n "$EXISTING_PIDS" ]; then
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
    echo "SWMM engine server is already running on ${HEALTH_URL}."
    echo "Existing PID(s): ${EXISTING_PIDS}"
    echo "Keep that terminal open, then use the HTML viewer."
    exit 0
  fi

  echo "Port ${PORT} is already in use by another process: ${EXISTING_PIDS}"
  echo "Stop it first, or run with another port:"
  echo "  SWMM_ENGINE_PORT=8766 ./Start_SWMM_Engine_Server.command"
  exit 1
fi

if ! python_has_pyswmm "$PYTHON_BIN"; then
  ./scripts/repair_pyswmm_macos_codesign.sh
fi

if [ "$MODE" = "legacy" ]; then
  exec "$PYTHON_BIN" server/swmm_engine_server.py --host "$HOST" --port "$PORT"
fi

exec "$PYTHON_BIN" server/swmm_fastapi_server.py --host "$HOST" --port "$PORT"
