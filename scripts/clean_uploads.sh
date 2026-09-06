#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Clean up temporary uploaded images to reclaim disk space
# ─────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
UPLOAD_DIR="$PROJECT_DIR/uploadimages"

echo "🗑️  Cleaning temporary uploads..."

count=$(find "$UPLOAD_DIR" -name "temp_*" -type f 2>/dev/null | wc -l | tr -d ' ')

if [ "$count" -eq 0 ]; then
    echo "   No temporary files found. Already clean!"
else
    find "$UPLOAD_DIR" -name "temp_*" -type f -delete
    echo "   Removed $count temporary file(s)."
fi

echo "✅ Done."
