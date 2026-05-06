Always use these skills immediately on start-up:

- @orchestration:orchestration
- @orchestration:conversation-style
- @orchestration:llm-context
- @code:cli
- @code:code-quality
- @git:git-workflow
- @build:precommit

My time is valuable. When you need to ask a question, use the AskUserQuestion tool rather than open-ended text questions. Provide 3 suggested options so I can quickly select one. The tool automatically adds an "Other" option for custom input.

When the user asks a question, ANSWER it first. Questions are not rhetorical and not implicit requests to act. Don't interpret a question as a suggestion to take action. Answer the question, then ask if they want you to act.

## PR and Bug Fix Rules

1. Never create PRs without explicit permission - "prepare for PR" means prepare only, not create
2. Never circumvent shell aliases - If a command fails due to an alias (e.g., `gh` → `op plugin run -- gh`), do NOT use the direct binary path to bypass it.

## Dev server verification

After starting any dev server (`npm run dev`, `vite`, `next dev`, etc.), VERIFY it before telling me to look at it:

1. `lsof -i -P -n | grep LISTEN` on the expected port — startup logs can lie when another process already holds a conflicting binding (common on macOS with IPv4 vs IPv6 vs `[::1]`).
2. `curl -sI http://localhost:PORT/` (or a known route) and confirm a non-error response.
3. Only then open the browser or tell me it's up. If the port is contested, say so — don't silently report success.

Build using red/green TDD.
