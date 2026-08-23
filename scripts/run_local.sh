#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

HOST="${SPORTRX_HOST:-127.0.0.1}"
PORT="${SPORTRX_PORT:-8501}"

echo "Starting SportRx on http://${HOST}:${PORT}"
echo "Use SPORTRX_HOST and SPORTRX_PORT to override the default local address."

python3 -m streamlit run app/streamlit_app.py \
  --server.address "$HOST" \
  --server.port "$PORT"
