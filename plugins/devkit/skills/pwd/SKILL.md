---
name: pwd
description: Print the full path of the current working directory.
when_to_use: When asked for the current working directory.
disable-model-invocation: true
allowed-tools:
  - Bash(pwd)
  - Bash(pwd *)
model: haiku
effort: low
---

# Print working directory

Reply with the following path exactly as written and nothing else: no code fence, no formatting, no
introduction, no explanation, and no insight block. This rule takes precedence over any output style.

!`pwd -W 2>/dev/null || pwd`
