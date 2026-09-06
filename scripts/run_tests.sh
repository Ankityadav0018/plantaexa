#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Run all project tests
# ─────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "🧪 Running Plantaexa tests..."
echo "────────────────────────────────────"

source .venv/bin/activate 2>/dev/null || true

python test_project.py -v

echo ""
echo "✅ All tests completed."
