---
name: explain
description: Explain a concept, technology, or piece of code at a chosen level, from a tldr of two or three
  sentences through eli5, beginner, and intermediate to expert depth.
when_to_use: When asked to explain something at a specific level of difficulty or detail.
argument-hint: "[tldr|eli5|beginner|intermediate|expert] <subject>"
disable-model-invocation: true
model: haiku
effort: medium
---

# Explain

Explain the subject in the following input at the requested level:

```text
$ARGUMENTS
```

When the input is empty, ask for a subject and stop.

## Parse the input

Match the first word case-insensitively against the five levels below.

- On a match, that word is the level and the rest of the input is the subject. `/explain expert the .NET
  garbage collector` asks for an expert-level explanation of the garbage collector.
- Without a match, the whole input is the subject and the level is `tldr`. `/explain async/await in C#` asks
  for a tldr.
- A level with nothing after it, as in `/explain eli5`, has no subject. Ask for one and stop.

A level word that begins the subject is always read as the level: `/explain expert systems` is an expert-level
explanation of "systems". Prefix an explicit level to keep the word, as in `/explain tldr expert systems`.

## Resolve the subject

Treat the subject as a concept or a technology unless one of these applies:

- It refers into the conversation, such as "the function above" or "this error". It then means the code or
  text it points at. When the conversation does not contain it, say what is missing and stop.
- It names code in the working directory: a path, a file name with an extension, a qualified or called
  identifier (`Foo.Bar`, `Baz()`), or a name qualified by "our", "this repo", or "in this project". Locate it
  with Glob or Grep. When nothing matches, say so and stop. When several locations match, keep all of them.

Do not search the working directory for a subject that reads as a concept.

## Levels

- **`tldr`** - for anyone in a hurry. Two or three sentences that state the core idea. No examples, caveats, or
  history.
- **`eli5`** - for a curious child. One or two paragraphs in which a single everyday analogy carries the whole
  explanation. No jargon, numbers, or code. Point out where the analogy breaks down only when it would
  otherwise leave a wrong idea behind.
- **`beginner`** - for someone new to the field. A few paragraphs that define every term on first use and
  include one small concrete example. No internals, alternatives, or edge cases.
- **`intermediate`** - for a practitioner who knows the basics. How it works, why it is designed that way, and
  the typical pitfalls, at whatever length that takes. Do not define basic terms.
- **`expert`** - for a peer. Precise terminology, internals, edge cases, and trade-offs against alternatives,
  at whatever length that takes. Do not define standard terms.

These rules apply at every level and take precedence over any general instruction on how to answer:

- Lead with the answer. No preamble, no restating the question, no closing offer to elaborate.
- Code examples, where the level allows them, are minimal and in the language the subject implies.
- When the subject is a framework, library, or language feature, `beginner` links the relevant official
  documentation, and `intermediate` and `expert` also quote the passage that supports the explanation.
  `tldr` and `eli5` carry no link. Include only URLs fetched and confirmed during this run; omit a link rather
  than guess one.

## Dispatch

The level decides who writes the explanation:

| Level          | Written by                 | `model`  | `effort` |
|----------------|----------------------------|----------|----------|
| `tldr`         | This skill, inline         | -        | -        |
| `eli5`         | `general-purpose` subagent | `sonnet` | `medium` |
| `beginner`     | `general-purpose` subagent | `sonnet` | `medium` |
| `intermediate` | `general-purpose` subagent | `sonnet` | `high`   |
| `expert`       | `general-purpose` subagent | `opus`   | `high`   |

For `tldr`, write the explanation directly. When the subject is code in the working directory, read it first.

For every other level, call the Agent tool with `subagent_type: general-purpose` and the `model` and `effort`
from the table. This skill sets both explicitly; do not omit `effort`. The subagent sees none of this
conversation, so its prompt must stand on its own:

- The subject, as resolved above.
- The level's entry from the Levels section and the rules that apply at every level, verbatim.
- Verbatim, any code, error text, or excerpt from the conversation that the subject refers to.
- For code in the working directory, the absolute paths of every match, so the subagent reads the code itself.
- These constraints, verbatim: "Return the explanation only. Do not modify files or run commands that change
  state. You cannot ask the user anything: when the subject is ambiguous, explain its most likely reading.
  Verify every documentation URL with WebFetch before citing it."

Wait for the result. The subagent's report is not shown to the user, so relay it unchanged: no summary, no
added introduction or comment, no edits. When the call fails or returns nothing, say so in one sentence and do
not write the explanation yourself.

## Output

The explanation and nothing else. The stop cases above, and a failed subagent call, reply with a single
sentence instead.
