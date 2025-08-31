- When a code change is ready, and we are about to return control to the user, do these things in order:
  - Remove obvious comments using the comment-cleaner agent
  - Verify the build passes using the precommit-runner agent
  - Commit to git using the git-commit-handler agent
  - Rebase on top of the upstream branch with the git-rebaser agent

- Don't run long-lived processes like development servers or file watchers
  - Don't run `npm run dev`
  - Echo copy/pasteable commands and ask the user to run it instead

- Use long flag names when using the Bash tool. For example:
  - Don't run `git commit -m`
  - Run `git commit --message` instead
