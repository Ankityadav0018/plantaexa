#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Quick setup script — creates venv and installs all deps
# ─────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "🌿 Plantaexa — Project Setup"
echo "────────────────────────────────────"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "📦 Virtual environment already exists."
fi

# Activate and install
echo "📥 Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "   Activate with:  source .venv/bin/activate"
echo "   Flask app:      python app.py"
echo "   Chatbot:        streamlit run chatbot/app.py"
echo "   Tests:          python test_project.py -v"
