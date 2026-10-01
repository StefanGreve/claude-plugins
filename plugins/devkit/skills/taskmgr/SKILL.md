---
name: taskmgr
description: Conventions for the todo.md task list at a repository root, covering how an entry is retired once
  its work is done.
when_to_use: Whenever a markdown file other than repository boilerplate is read or edited, and whenever a task
  tracked in todo.md is finished.
user-invocable: false
paths:
  - "**/*.md"
  - "!**/readme.md"
  - "!**/changelog.md"
  - "!**/license.md"
  - "!**/licence.md"
  - "!**/contributing.md"
  - "!**/code_of_conduct.md"
  - "!**/security.md"
  - "!**/authors.md"
  - "!**/notice.md"
---

# Task management

Tasks live in a `todo.md` file at the repository root. It is git-ignored through the `todo*.md` pattern in the
global gitignore, so it never appears in a commit, in a commit message, or in a list of changed files.

## Retiring a finished entry

When a task is finished, delete its entry outright, including the title and every detail line. Never mark it
`- [x]`, and never ask permission first: the deletion is part of finishing the task, not a separate decision.

Three cases need more than a plain deletion:

- **Partially finished.** When only some bullets of a multi-bullet entry are done, delete those and leave the
  rest.
- **Right goal, wrong approach.** When the entry's proposed approach turned out to be wrong but its goal was
  achieved anyway, delete the entry and explain in chat why the approach did not work.
- **Overtaken by other work.** When the entry turns out to be already resolved elsewhere, or not worth doing
  at all, delete it and say which of the two it was.

A deletion is reported, never silent. State in chat which entry was removed and under which of the cases
above, so the file and the conversation agree.
