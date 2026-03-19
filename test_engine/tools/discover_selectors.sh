#!/usr/bin/env bash
# Wrapper para discover_selectors.py
# Uso: bash test_engine/tools/discover_selectors.sh [--url URL] [--login-path PATH] [--no-headless]
#
# Em Replit/NixOS define PLAYWRIGHT_BROWSERS_PATH para reutilizar os browsers do .NET:
#   PLAYWRIGHT_BROWSERS_PATH=/home/runner/workspace/.cache/ms-playwright \
#   bash test_engine/tools/discover_selectors.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! python3 -c "import playwright" 2>/dev/null; then
    echo "A instalar playwright..."
    pip install -r "${SCRIPT_DIR}/requirements.txt" -q
fi

exec python3 "${SCRIPT_DIR}/discover_selectors.py" "$@"
