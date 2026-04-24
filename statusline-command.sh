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

PART1=$(echo "$INPUT" | npx -y @owloops/claude-powerline@1.25.2 --theme=tokyo-night --style=capsule)
# Strip context_window to force transcript-based calculation (workaround for anthropics/claude-code#13783)
PART2=$(echo "$INPUT" | jq 'del(.context_window)' | npx -y ccusage@18.0.11 statusline --visual-burn-rate emoji)

# Task count from .llm/todo.md (only displayed if > 0)
CWD=$(echo "$INPUT" | jq -r '.cwd // .workspace.current_dir // empty')
TASK_COUNT=""
if [[ -n "$CWD" && -f "$CWD/.llm/todo.md" ]]; then
    COUNT=$(grep -c '^- \[ \]' "$CWD/.llm/todo.md" 2>/dev/null || echo 0)
    if [[ "$COUNT" -gt 0 ]]; then
        TASK_COUNT=" 📋 $COUNT"
    fi
fi

# Rate limits (5-hour and 7-day windows)
FIVE=$(echo "$INPUT" | jq -r '.rate_limits.five_hour.used_percentage // empty')
WEEK=$(echo "$INPUT" | jq -r '.rate_limits.seven_day.used_percentage // empty')
RATE=""
[[ -n "$FIVE" ]] && RATE=" ⏱ 5h:$(printf '%.0f' "$FIVE")%"
[[ -n "$WEEK" ]] && RATE="${RATE} 7d:$(printf '%.0f' "$WEEK")%"

echo -e "$PART1$TASK_COUNT\n$PART2$RATE"
