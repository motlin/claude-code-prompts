🔁 Process all todos automatically

Continuously work through all incomplete tasks in `.llm/todo.md` until none remain.

## How it works

This command runs a loop that:
1. Checks if there are any incomplete tasks using `todo-get $(git rev-parse --show-toplevel)/.llm/todo.md`
2. If a task is found, launches the `do-todo` agent to implement it
3. Repeats until no incomplete tasks remain

## Process flow

```
while todo-get returns a task:
    → Launch `do-todo` agent
    → Agent implements the task
    → Agent marks task complete
    → Agent runs precommit tests
    → Agent commits changes
    → Loop continues with next task
```

## Important notes

- Each task is handled completely by the `do-todo` agent before moving to the next
- The loop stops when `todo-get` returns nothing (all tasks complete)
- Each task gets its own commit for clear history
- Tasks marked as `[>]` (in progress elsewhere) are skipped
