#!/bin/bash
# Serve all Claude plans as HTML with auto-refresh index.
# Auto-shuts down after 24 hours.

set -euo pipefail

PORT=8899
PLANS_DIR="${HOME}/.claude/plans"
MAX_AGE_SECONDS=86400

if [ ! -d "$PLANS_DIR" ]; then
    echo "No plans directory found at $PLANS_DIR" >&2
    exit 1
fi

# Kill any existing server on the port
lsof -ti:"$PORT" 2>/dev/null | xargs kill 2>/dev/null || true
sleep 0.3

# Start the server
python3 ~/.claude/scripts/plan-server.py "$PLANS_DIR" "$PORT" &
SERVER_PID=$!

# Schedule auto-shutdown after 24 hours
(sleep "$MAX_AGE_SECONDS" && kill "$SERVER_PID" 2>/dev/null) &

echo "$SERVER_PID"
