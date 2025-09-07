✅ Find and implement the next incomplete task from the project todo list.

## Steps

- Find the next incomplete task
  - Run `todo-get $(git rev-parse --show-toplevel)/.llm/todo.md`
  - It returns the first `Not started` task

- Implement the task
- Think hard about the plan
- Focus ONLY on implementing this specific task
- Ignore TODOs in the source code
- Work through the implementation methodically and completely, addressing all aspects of the task
- Run appropriate tests and validation to ensure the implementation works

- When a code change is ready, and we are about to return control to the user, do these things in order:
  - Remove obvious comments using the @comment-cleaner agent
  - Verify the build passes using the @precommit-runner agent
  - Commit to git using the @git-commit-handler agent
  - Rebase on top of the upstream branch with the @git-rebaser agent

- ✅ Finally mark the task as complete:
  - Run `todo-complete $(git rev-parse --show-top-level)/.llm/todo.md`
  - It marks the first incomplete task as `[x]`

## Todo context
The task list is in `.llm/todo.md`. You will not use the Read tool on this file. You'll interact with it through the `todo-get` and `todo-complete` commands. The format is:

```markdown
- `[ ]` - Not started
- `[x]` - Completed
- `[>]` - In progress in a peer directory/worktree
```

