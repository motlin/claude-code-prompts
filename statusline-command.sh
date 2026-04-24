#!/bin/bash

# Read JSON input from stdin
INPUT=$(cat)

# Cache the raw JSON for the web dashboard
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
if [[ -n "$SESSION_ID" ]]; then
    CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/claude-code-plans/statusline"
    mkdir -p "$CACHE_DIR"
    echo "$INPUT" >"$CACHE_DIR/$SESSION_ID.json"
fi

CWD=$(echo "$INPUT" | jq -r '.cwd // .workspace.current_dir // empty')
if [[ -n "$CWD" ]]; then
    COUNT=$(grep -c '^- \[ \]' "$CWD/.llm/todo.md" 2>/dev/null || echo 0)
    [[ "$COUNT" -gt 0 ]] && export TASKS="$COUNT"
fi

echo "$INPUT" | npx -y @owloops/claude-powerline@1.25.2 --theme=tokyo-night --style=capsule
