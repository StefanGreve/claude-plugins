---
name: propose
description: Propose 10 alternatives for a given input, such as rewordings of a sentence, variations of a
  point, or different implementations of a code fragment.
when_to_use: When asked for alternative wordings, phrasings, names, points, or implementations of a specific
  piece of text or code.
argument-hint: "<text>"
disable-model-invocation: true
model: haiku
effort: medium
---

# Propose

Return 10 alternatives for the following input:

```text
$ARGUMENTS
```

When the input is empty, ask for it and stop.

## Establish the target

The target is the text or code the alternatives replace.

- By default the whole input is the target. `/propose The cache is flushed on every write` asks for 10 other
  ways to write that sentence.
- When the input states what is to be reworded, only that part is the target and the rest is instruction or
  context. `/propose a better name for GetUserDataFromDb` asks for 10 names, not 10 rewordings of the
  request. `/propose the second sentence of the summary above` points at text in the conversation.
- When the input refers to something that the conversation does not contain, say what is missing and stop
  rather than guess.

## Match the kind of the target

The alternatives are of the same kind as the target and can replace it where it stands.

- A word, name, or identifier yields words, names, or identifiers, in the casing convention of the original.
- A sentence or paragraph yields rewordings that keep the meaning, the language, and the terminology of the
  original. Do not translate, and do not add or drop claims.
- A point or argument yields other points that serve the same purpose, not the same point in other words.
- Code yields implementations with the same observable behavior and signature, in the same language.

Constraints stated in the input, such as a tone, a length limit, or a library to avoid, apply to every
alternative.

## Make the alternatives distinct

Ten near-duplicates are one alternative. Vary what can vary for the kind of target: sentence structure,
length, register, and emphasis for prose; the angle for a point; the algorithm, control flow, or API for
code. Swapping a single synonym does not make a new alternative. Do not repeat the original.

## Output

A numbered list from 1 to 10 and nothing else: no introduction, no ranking, no recommendation, no closing
remark. Prose alternatives stand as plain list items. Each code alternative goes in a fenced code block under
its number, preceded by a line of at most ten words naming what distinguishes it.
