---
name: research
description: Research a question with up to three parallel subagents and collect the findings in
  research-<short-topic>.md.
when_to_use: When asked to research a topic, compare options, or gather facts before planning a feature.
argument-hint: "<research question>"
disable-model-invocation: true
model: opus
effort: max
---

# Research

Research the question in the following input:

```text
$ARGUMENTS
```

When the input is empty, ask for a question and stop.

## Output

- **File name.** `research-<short-topic>.md`, where `<short-topic>` names the topic in two to four lowercase
  words joined by hyphens. When a file with that name already exists, continue it; do not start a second file
  on the same topic.
- **Location.** The repository root, or the working directory outside a git repository.
- **Shape.** `${CLAUDE_SKILL_DIR}/assets/research-template.md`. Every region between `<!-- begin:<id> -->` and
  `<!-- end:<id> -->` is written through the script below, never by hand. The markers stay in the file so that
  a later run can update it.
- **Reply.** Once the file is complete, reply with its path.

## Script

`${CLAUDE_SKILL_DIR}/scripts/upsert.py` writes the file. Run it with `python`, or with `python3` where `python`
is missing. Pass section bodies on stdin through a quoted heredoc.

```sh
python <script> init <file> --title "<topic>" --question "<the question as given>"
python <script> section <file> <id> [--parent <id>] <<'EOF'
<markdown body>
EOF
python <script> source <file> --source "<url or path>" --confirms "<the fact it confirms>"
python <script> list <file>
```

`init` does nothing when the file exists. `section` replaces the body of `<id>`, or creates the region at the
end of `--parent`, which defaults to `threads`. `source` adds or updates one Sources row, keyed by `--source`.
`list` prints every region with the first line of its body. Every call locks the file, so parallel calls from
subagents are safe.

## Source order

Every thread starts with the files on disk: the source code, tests, configuration, documentation, and the git
history of the working directory. Source code of dependencies that is present on disk, such as a package cache
or a vendored copy, counts as on disk too. Turn to the web only for what these files cannot settle, for example
the intended behavior of an external API, the changes in a release, or a known issue upstream. Before citing a
web source, name the question that the files on disk left open.

## Threads

Run `init`. When the file already existed, run `list` and research only what its threads leave open.

Split the question into one to three independent threads, and use fewer when the question is narrow. Give each
thread a heading and an id of the form `thread-<kebab-case>`, such as `thread-rate-limits`.

Spawn the subagents for all threads in a single message, each with `subagent_type: general-purpose`,
`model: opus`, and `effort: max`. Spawn at most three subagents per invocation, retries included.

A subagent sees none of this conversation, so its prompt must stand on its own:

- The question, the thread's heading and id, and what the thread must settle.
- The absolute paths of the research file and of `upsert.py`, and the commands from the Script section.
- The thread block format, verbatim:

  ```markdown
  ### <Thread heading>

  **Status:** in progress | done | blocked

  - <Finding. Name the source that confirms it, as listed in Sources.>

  **Confidence:** <high, medium, or low>, because <reason>.
  **Gaps:** <what this thread could not settle, on disk or on the web, or "None.">
  ```

- These rules, verbatim: "Upsert your thread with `Status: in progress` before you start. Search the working
  directory first, including the source of dependencies on disk, and use WebSearch or WebFetch only for a
  question that the files on disk cannot settle. Name that question in your findings before citing a web source
  for it. Upsert each source as soon as you have confirmed it. Finish by upserting the complete thread block
  with `Status: done`, or with `Status: blocked` and the reason. Cite only URLs you fetched and files you read
  during this run. Do not modify any file except through upsert.py. Return a one-paragraph summary of your
  thread."

## Synthesis

Wait until every subagent has finished, then read the file. When a subagent ended without a finished thread
block, upsert its block with `Status: blocked` and the reason.

Write `answer` through the script. It starts with the direct answer to the question, then connects the threads
and names the sources that carry each conclusion. Write `open-questions` from the threads' gaps and every
blocked thread, or keep "None yet." when nothing is open.
