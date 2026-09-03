#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

HOST="${SPORTRX_HOST:-127.0.0.1}"
PORT="${SPORTRX_PORT:-8501}"
DEVELOPER_MODE="${SPORT_RX_DEVELOPER_MODE:-1}"

echo "Starting SportRx on http://${HOST}:${PORT}"
echo "Use SPORTRX_HOST and SPORTRX_PORT to override the default local address."
if [[ "$DEVELOPER_MODE" == "1" ]]; then
  echo "Local developer access is enabled; registration and login are skipped."
else
  echo "Account-flow testing is enabled; registration and login are required."
fi

SPORT_RX_DEVELOPER_MODE="$DEVELOPER_MODE" python3 -m streamlit run app/streamlit_app.py \
  --server.address "$HOST" \
  --server.port "$PORT"
