#!/bin/bash

# Read JSON input from stdin
INPUT=$(cat)

PART1=$(echo "$INPUT" | npx -y @owloops/claude-powerline@latest --theme=tokyo-night --style=capsule)
PART2=$(echo "$INPUT" | npx -y ccusage@latest statusline --visual-burn-rate emoji)

echo -e "$PART1\n$PART2"
