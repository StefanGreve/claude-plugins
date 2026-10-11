---
name: commit-message
description: Write a git commit message in Stefan's conventions, using the short single-line form by default
  and the verbose summary-plus-bullets form when `verbose` is requested, with a Co-authored-by trailer on
  verbose messages when Claude wrote the majority of the code.
when_to_use: After completing a task in a git repository, or whenever asked to suggest, write, reword, or
  review a commit message.
argument-hint: "[atomic] [short|verbose]"
model: haiku
effort: medium
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git check-ignore:*)
---

# Commit message

Suggest a commit message in chat. Do not run `git commit` unless explicitly asked to; this skill produces the
message, not the commit.

## Establish what the commit records

The invoker stages what they want committed, so the index defines the message. Run `git status --short` for
the shape of the tree, then `git diff --staged` to read the change itself. Describe the staged set and
nothing else.

- When nothing is staged, say so and stop. Do not fall back to `git diff` and describe the working tree: with
  an empty index there is no commit to name, and a message written against unstaged work will not match what
  eventually lands.
- Unstaged and untracked paths stay out of the message, however relevant they look. They belong in the
  suggestion that follows it.
- A staged file you did not write is still part of the commit. Staging is the filter, not authorship.
- Skip git-ignored files. `todo.md` and `notes.md` are ignored globally and never belong in a message.
  `git check-ignore -v <path>` settles any doubt.
- When the staged set spans unrelated concerns, write the message for all of it and say that it does. That is
  the case `atomic` below exists to handle.

## Choose the form

The invocation selects the form. `verbose` selects the verbose form; `short`, or no form argument at all,
selects the short form. Do not switch to the verbose form because the change is large: the size of the diff
has no bearing on the form.

**Short** - a single-line summary. This is the default. A large change still gets one line, which names the
dominant intent of the change rather than listing its parts.

```text
Strip comment
```

**Verbose** - a summary line, a blank line, then `*` bullet points. Use it only when the invocation includes
`verbose`.

```text
Harden Claude Code settings for macOS and Windows

* Drop CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC from the env block: the
  variable is read for presence only, so "0" still kept essential-traffic
  mode on and blocked /schedule. Unsetting it is the only way to turn it off
* Set disableBypassPermissionsMode to "disable" so bypassPermissions can no
  longer be selected
```

## Summary line

- Imperative mood, capitalised, no trailing period.
- At most 72 characters.
- No `type(scope):` prefix. This project does not follow Conventional Commits.
- A `Subject: detail` prefix is available when it genuinely narrows the scope, as in
  `Update CLAUDE.md: refine language output`. Do not reach for it by default.

## Bullets

These rules apply to the verbose form only.

- One `* ` per bullet, continuation lines indented by two spaces.
- No blank line between bullets, no trailing period.
- Wrap body lines at roughly 80 characters.
- State the cause or the consequence alongside the change, not just the change. Make the subject, the action,
  and any temporal or causal relationship explicit:
  - `Name pwsh.exe by absolute path, since Task Scheduler resolves the action against the service PATH and
    cannot see the per-user WindowsApps alias`
  - `Write the start boundary as local time without a UTC offset, so the reminder keeps its wall clock time
    across daylight saving transitions`
- A bullet that only restates its diff carries no information. Explain why the change was needed, or what it
  now makes possible.

## Trailer

When Claude wrote the majority of the code, end a verbose message with a trailer naming the model that wrote
it, separated from the bullets by a blank line:

```text
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

This skill runs on Haiku whatever the session model is, so the model you are running as is not necessarily
the one that wrote the code. Name the model only when the conversation establishes which one wrote the code;
otherwise omit the trailer rather than guess. The short form takes no trailer.

## Atomic commits

When the invocation includes `atomic`, judge whether the staged set is one change or several before writing
anything. Where it divides cleanly along lines of intent - a bug fix beside an unrelated rename, a dependency
bump beside the feature that needed it - propose one commit per concern rather than a single message.

- Give each proposed commit its paths and its own message, written to the rules above and in the form the
  invocation selected.
- Order them so that every commit leaves the tree in a working state. A commit that only compiles once a
  later one lands is not atomic, merely split.
- Follow the proposals with the `git restore --staged` and `git add` commands that carve the present index
  down to the first commit. Suggest them; do not run them.

When the staged set is already one coherent change, say so and suggest the single message. Splitting a change
whose parts only make sense together is worse than leaving it whole.

## Suggest what else belongs in the commit

After the message, name any unstaged path the staged change left incomplete: a test for the new function, a
stale `CHANGELOG.md` or `README.md` entry. One line each, then stop.

Say nothing about the rest of the working tree. Scratch files, editor directories, and unrelated work in
progress are noise the invoker left unstaged on purpose. Having nothing to add is the ordinary case.
