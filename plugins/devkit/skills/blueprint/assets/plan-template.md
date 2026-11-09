# Plan: <feature or change, in a few words>

Retires the `<entry title>` entry under `<section>` in `todo.md`. Every step below stands on its own: it names
the files, the change, how to verify it, and what "done" looks like, so the work can stop and resume between
any two steps with the suite green.

<!--
How to use this template:

- Replace every <placeholder>. Delete a section that has nothing to say rather than leaving it empty.
- Drop the sentence about `todo.md` below the title when no entry there tracks the change.
- Build the Contents list from the final headings, so that every link matches the anchor of its heading.
- Write the plan before the first edit, and update it when a step lands differently than planned, so the file
  stays the record of what was decided and why.
- Keep lines at 120 characters and the file ASCII only.
- Research sections (the two after Goal) exist so that a step never rests on memory: each fact names where it
  was confirmed and when. Drop them for a change that needs no outside input.
- A step is the unit of work and of review. If a step cannot be verified on its own, split it.
- Keep the `<!-- References -->` marker. Below it, define one reference link per cited source, and delete the
  `[<label>]: <url>` line when the plan cites none.
-->

## Contents

- [Plan: <feature or change, in a few words>](#plan-feature-or-change-in-a-few-words)
  - [Contents](#contents)
  - [Goal](#goal)
  - [What <the source> contributes](#what-the-source-contributes)
  - [What was verified about <the dependency>](#what-was-verified-about-the-dependency)
  - [Decisions](#decisions)
  - [Step 1: <name>](#step-1-name)
  - [Step N: <name>](#step-n-name)
  - [Out of scope](#out-of-scope)
  - [Open assumptions](#open-assumptions)

## Goal

<Two or three paragraphs. What the finished change does from the user's point of view, which existing path it
follows (name the precedent in the code base), and what it deliberately leaves alone. State what already
exists that the change builds on, with the file or the test that proves it.>

## What <the source> contributes

<For a change prompted by an article, an issue, or another project: what carries over and what does not, each
with the reason. A reader should be able to tell which of the source's ideas the plan adopted and why the rest
were set aside.>

Carry over:

- **<Idea>.** <Why it applies here, and which step uses it.>

Do not carry over:

- **<Idea>.** <Why it does not apply here. Name the constraint, such as the runtime, the deployment, or a
  documented principle of the project.>

## What was verified about <the dependency>

Checked on <YYYY-MM-DD> against <the published package, the documentation, the live service>, so that
step <N> does not rest on memory:

| Fact                                              | Where it was confirmed                        |
| ------------------------------------------------- | --------------------------------------------- |
| <Fact a step depends on>                          | <URL, file, command output>                   |
| <Fact a step depends on>                          | <URL, file, command output>                   |

<One paragraph on what the table settles, such as a URL shape, a version, or an API that a step calls.>

## Decisions

Each is a choice the steps below assume. Reopen one here before changing a step that depends on it.

1. **<Decision>.** <The reason, the precedent it follows, and the alternative it rules out.>
2. **<Decision>.** <...>

## Step 1: <name>

**Files**

- `<path>`
- <Every file that repeats a pattern, described once: "every test that constructs an X by initializer, which
  today is A, B and C">

**Change**

- <What changes, precise enough to execute without re-deriving it. Quote the signature, the key, the snippet.>
- <What does not need to change, and why, when a reader might expect it to.>

**Verify**

```sh
<the commands>
```

<What to look for in the output, or in the browser, including what is expected to be absent.>

**Done when** <one sentence a reviewer can check: the suite is green at N, the output contains X, a grep lists
the same files for both of two symbols.>

## Step N: <name>

<Same four parts. Later steps may name what an earlier step left temporary, such as a key added for a check,
and say which step removes it or makes it permanent.>

## Out of scope

- **<Item>.** <Why it is left out, and where it is recorded, such as a new entry in `todo.md`.>

## Open assumptions

Each is believed true and is checked at the step named. A wrong one changes that step, not the plan.

- <Assumption.> Checked in step <N> by <observation>; the fallback is <alternative>.

<!-- References -->

[<label>]: <url>
