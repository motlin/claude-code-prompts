---
allowed-tools: Bash(git:*), Read, Edit
description: Conceptually apply changes from a specific commit to current HEAD
---

🍒 Conceptually apply changes from a specific commit: $ARGUMENTS, to the current HEAD.

Instead of using `git cherry-pick <SHA>`, inspect the specified commit and recreate the same changes on the current HEAD.

- Examine the changes in the commit
- Apply similar changes to the current working directory
Create a new commit using `git commit -c <SHA>`

