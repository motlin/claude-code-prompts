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
    TODO="$CWD/.llm/todo.md"
    COUNT=$(grep -c '^- \[ \]' "$TODO" 2>/dev/null) || COUNT=0
    BLOCKED=$(grep -c '^- \[!\]' "$TODO" 2>/dev/null) || BLOCKED=0

    # claude-powerline accepts one env segment per line, so both counts share
    # TASKS. Each carries its own icon and appears only when non-zero, and the
    # segment's own prefix is empty so neither icon labels the other's count.
    PARTS=()
    [[ "$COUNT" -gt 0 ]] && PARTS+=("📋 $COUNT")
    [[ "$BLOCKED" -gt 0 ]] && PARTS+=("⚠ $BLOCKED")
    [[ "${#PARTS[@]}" -gt 0 ]] && export TASKS="${PARTS[*]}"
fi

echo "$INPUT" | npx -y @owloops/claude-powerline@1.25.2
