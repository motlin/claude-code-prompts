📝 Commit the local changes to git. Analyze my local changes and propose splitting them into multiple logical commits.

- 📦 Stage files or parts of files individually
  - Only stage changes that you remember editing yourself.
  - Avoid commands like `git add .` and `git add -A` and `git commit -am` which stage all changes
- Use single quotes around file names containing `$` characters
  - Example: `git add 'app/routes/_protected.foo.$bar.tsx'`
- Commit messages should:
  - Start with a present-tense verb (Fix, Add, Implement, etc.)
  - Not include adjectives that sound like praise (comprehensive, best practices, essential)
  - Be concise (60-120 characters)
  - Be a single line
  - Sound like the title of the issue we resolved, and not include the implementation details we learned during implementation
  - End with a period.
  - Describe the intent of the original prompt
- If pre-commit hooks fail, then there are now local changes
  - `git add` those changes and try again
  - Never use `git commit --no-verify`

For each proposed commit, show me the message and the list of files. Show all proposals at once. Wait for my confirmation, then commit all.
