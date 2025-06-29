# Create Git Worktree for Next Available Todo

You are to create a new git worktree in a peer directory for the first available todo item (not completed and not already in progress).

## Todo Status Icons:
- `[ ]` - Not started
- `[x]` - Completed
- `[>]` - In progress in a peer directory/worktree

## Steps to follow:

1. **Find the next available todo**:
   - Look for the first todo that is marked with `[ ]` (not `[x]` or `[>]`)
   - This will be the todo to work on
   - If no available todos exist, inform the user that all todos are either completed or in progress

2. **Update the todo status**:
   - Change the selected todo from `[ ]` to `[>]` in the original todo list
   - Add a comment indicating which worktree it's being worked on in, e.g.:
     ```markdown
     - [>] Implement user authentication with JWT <!-- worktree: implement-user-auth-jwt -->
     ```

3. **Create the git worktree**:
   - Determine the current repository's root directory
   - Create a worktree name based on the todo item (use kebab-case)
   - Create the worktree in a peer directory: `git worktree add ../<worktree-name> -b <branch-name>`
   - The `<branch-name>` should be prefixed with `task/`
   - The `<worktree-name>` should start with the original repository's directory name

4. **Set up the todo file in the new worktree**:
   - Navigate to the new worktree directory
   - Create the directory `.llm` if it doesn't exist
   - Create `.llm/todo.md` with ONLY this single todo item:

```markdown
# Todo

- [ ] [Single todo item text here]

## Original Location
Todo list: [filename and line number where this todo was found]

When this task is complete:
1. Find the main repository: `git rev-parse --git-common-dir`
2. Navigate to the main repository
3. Update the todo status from `[>]` to `[x]`
4. Remove or update the worktree comment
5. Delete this worktree: `git worktree remove <current-worktree-path>`
```
