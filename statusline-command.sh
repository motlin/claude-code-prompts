#!/bin/bash

# Read JSON input from stdin
INPUT=$(cat)

PART1=$(echo "$INPUT" | npx -y @owloops/claude-powerline@latest --theme=tokyo-night --style=capsule)
# Strip context_window to force transcript-based calculation (workaround for anthropics/claude-code#13783)
PART2=$(echo "$INPUT" | jq 'del(.context_window)' | npx -y ccusage@latest statusline --visual-burn-rate emoji)

# Task count from .llm/todo.md (only displayed if > 0)
CWD=$(echo "$INPUT" | jq -r '.workspace.cwd // empty')
TASK_COUNT=""
if [[ -n "$CWD" && -f "$CWD/.llm/todo.md" ]]; then
    COUNT=$(grep -c '^- \[ \]' "$CWD/.llm/todo.md" 2>/dev/null || echo 0)
    if [[ "$COUNT" -gt 0 ]]; then
        TASK_COUNT=" 📋 $COUNT"
    fi
fi

echo -e "$PART1$TASK_COUNT\n$PART2"
