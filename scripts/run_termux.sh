#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")/.."
if [ ! -d .venv ]; then echo "Execute primeiro: bash scripts/termux_setup.sh"; exit 1; fi
source .venv/bin/activate
export PYTHONPATH="$PWD"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
