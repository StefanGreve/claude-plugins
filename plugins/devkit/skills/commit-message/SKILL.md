---
name: commit-message
description: Write a git commit message in Stefan's conventions, using the one-line `minimal` form by default
  and the bulleted `normal`, `verbose`, or `detailed` forms on request, with a Co-authored-by trailer on
  multiline messages when Claude wrote the majority of the code.
when_to_use: After completing a task in a git repository, or whenever asked to suggest, write, reword, or
  review a commit message.
argument-hint: "[atomic] [minimal|normal|verbose|detailed]"
model: haiku
effort: medium
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git branch:*)
  - Bash(git check-ignore:*)
---

# Commit message

Return the commit message and nothing else: a single fenced `text` block, with no preamble, explanation, or
follow-up. The invoker copies it as is, so anything around it is noise. Two cases are exempt: an empty index,
which gets one sentence instead, and `atomic`, which keeps the output described in its section.

Do not run `git commit` unless explicitly asked to; this skill produces the message, not the commit.

## Read the repository's conventions

Run `git branch --show-current` and `git log -10 --format=%s` before writing anything. The rules below are
defaults; the history shows what this repository actually does.

- Look for patterns the subjects share: ticket prefixes (`ABC-123: `, `[ABC-123] `, `#123 `), Conventional
  Commits `type(scope):` prefixes, capitalization, and language.
- When the history prefixes subjects with ticket references and the branch name carries one, as in
  `feature/ABC-123-export-csv`, prefix the summary with that ticket in the format the history uses. A ticket
  in the branch name alone is not a convention; without the matching history, leave it out.
- A pattern counts as a convention when most of the ten subjects follow it, not when a single one does. Where
  a convention is clear, it overrides the summary line rules below. Where the history is mixed or silent,
  apply those rules as written.

## Establish what the commit records

The invoker stages what they want committed, so the index defines the message. Run `git status --short` for
the shape of the tree, then `git diff --staged` to read the change itself. Describe the staged set and
nothing else.

- When nothing is staged, reply with one sentence saying so and stop. Do not fall back to `git diff` and
  describe the working tree: with an empty index there is no commit to name, and a message written against
  unstaged work will not match what eventually lands.
- Unstaged and untracked paths stay out of the message, however relevant they look.
- A staged file you did not write is still part of the commit. Staging is the filter, not authorship.
- Skip git-ignored files. `todo.md` and `notes.md` are ignored globally and never belong in a message.
  `git check-ignore -v <path>` settles any doubt.
- When the staged set spans unrelated concerns, write one message that covers all of it. Splitting it is the
  case `atomic` below exists to handle.

## Choose the form

The invocation selects the form; without a form argument, use `minimal`. Do not switch to a longer form
because the change is large: the size of the diff has no bearing on the form.

| Form       | Body                                         | Bullets               | Lines per bullet |
|------------|----------------------------------------------|-----------------------|------------------|
| `minimal`  | Summary line only                            | none                  | -                |
| `normal`   | Summary line, blank line, bullets            | 2-3                   | 1-2              |
| `verbose`  | As `normal`                                  | up to 4, prefer fewer | 2-3              |
| `detailed` | As `verbose`, plus an optional ASCII diagram | up to 6               | 3-5              |

The limits are ceilings, not quotas. Never pad a bullet to reach a line count, and when a change has less to
say than the form allows, write fewer bullets in the requested form rather than switching to another.

**minimal** - a single-line summary. A large change still gets one line, which names the dominant intent of
the change rather than listing its parts.

```text
Strip comment
```

**normal** - a summary line, a blank line, then two or three `*` bullets of one or two lines each.

```text
Pin pwsh to its absolute path in the reminder task

* Task Scheduler resolves actions against the service PATH, which cannot see
  the per-user WindowsApps alias
* Keep the working directory unset so relative paths fail loudly
```

**verbose** - as `normal`, but each bullet runs two to three lines and the message holds at most four
bullets. Prefer fewer when they cover the change.

```text
Harden Claude Code settings for macOS and Windows

* Drop CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC from the env block: the
  variable is read for presence only, so "0" still kept essential-traffic
  mode on and blocked /schedule. Unsetting it is the only way to turn it off
* Set disableBypassPermissionsMode to "disable" so bypassPermissions can no
  longer be selected
```

**detailed** - as `verbose`, but each bullet runs three to five lines and the message holds at most six
bullets. Add an ASCII diagram only when it shows structure that prose conveys poorly, such as a data flow, a
state transition, or a directory layout; most detailed messages need none. Place it after the bullets,
separated by a blank line, indent it by two spaces, and keep its lines within 80 characters.

```text
Route reminder output through the shared log writer

* Write task output through LogWriter instead of redirecting stdout, since
  Task Scheduler discards the redirect when the action runs without an
  interactive session, which left failed runs without any trace
* Send errors to both the log file and the Application event log, so a
  failure stays visible even when the log directory is missing or locked
  by another process

  Reminder.ps1 --> LogWriter --+--> %LOCALAPPDATA%\Reminder\reminder.log
                               |
                               +--> Application event log (errors only)
```

## Summary line

A convention read from the repository's history takes precedence over the rules in this section.

- Imperative mood, capitalized, no trailing period.
- At most 72 characters, including any ticket prefix.
- No `type(scope):` prefix, unless the repository's history uses one.
- A `Subject: detail` prefix is available when it genuinely narrows the scope, as in
  `Update CLAUDE.md: refine language output`. Do not reach for it by default.

## Bullets

These rules apply to every form except `minimal`.

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

When Claude wrote the majority of the code, end a multiline message with a trailer naming the model that wrote
it, separated from the bullets by a blank line:

```text
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

This skill runs on Haiku whatever the session model is, so the model you are running as is not necessarily
the one that wrote the code. Name the model only when the conversation establishes which one wrote the code;
otherwise omit the trailer rather than guess. The `minimal` form takes no trailer.

## Atomic commits

When the invocation includes `atomic`, judge whether the staged set is one change or several before writing
anything. Where it divides cleanly along lines of intent - a bug fix beside an unrelated rename, a dependency
bump beside the feature that needed it - propose one commit per concern rather than a single message. This
mode is exempt from the message-only rule and returns the output described here.

- Give each proposed commit its paths and its own message, written to the rules above and in the form the
  invocation selected.
- Order them so that every commit leaves the tree in a working state. A commit that only compiles once a
  later one lands is not atomic, merely split.
- Follow the proposals with the `git restore --staged` and `git add` commands that carve the present index
  down to the first commit. Suggest them; do not run them.

When the staged set is already one coherent change, say so and suggest the single message. Splitting a change
whose parts only make sense together is worse than leaving it whole.
