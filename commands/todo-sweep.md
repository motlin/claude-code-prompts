name: todo-sweep
description: Find all TODO comments and create background tasks for each

---

Search the codebase for all TODO comments and create a task list entry for each one. Each TODO will be handled as a background task using the Task tool. The task description will include the full text of the TODO comment line found in the code.

The search will:
1. Find all occurrences of "TODO" in the codebase
2. Create a todo list entry for each TODO found
3. Include the complete TODO comment text in the task description
4. Mark each as a background task to be processed with the Task tool

Example output:
```
/todos
  ⎿  2 todos:

     ☐ Handle in background task: Implement the todo comment in code "// TODO: Extract commonality in getRootNodes and getChildNodes" in src/api/client.ts:87

     ☐ Handle in background task: Implement the todo comment in code "// TODO: Use deep object equality rather than loose assertions" in test/utils.test.ts:103
```