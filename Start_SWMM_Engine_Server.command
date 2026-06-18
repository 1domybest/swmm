#!/bin/zsh
set -u

cd "$(dirname "$0")" || exit 1

HOST="${SWMM_ENGINE_HOST:-127.0.0.1}"
PORT="${SWMM_ENGINE_PORT:-8765}"
HEALTH_URL="http://${HOST}:${PORT}/health"
PYTHON_BIN="python3"

if [ -x ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
fi

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

if ! "$PYTHON_BIN" -c "import pyswmm" >/dev/null 2>&1; then
  ./scripts/repair_pyswmm_macos_codesign.sh
fi

exec "$PYTHON_BIN" server/swmm_engine_server.py --host "$HOST" --port "$PORT"
