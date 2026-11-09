---
name: blueprint
description: Write a plan for a feature to plan-<short-feature-name>.md in the shape of the bundled plan
  template.
when_to_use: When asked to plan a feature or to write a plan file for one.
argument-hint: "<feature description>"
disable-model-invocation: true
model: opus
effort: max
---

# Blueprint

Write a plan for the feature described in the following input:

```text
$ARGUMENTS
```

When the input is empty, ask for a feature description and stop.

## Output

- **File name.** `plan-<short-feature-name>.md`, where `<short-feature-name>` names the feature in two to four
  lowercase words joined by hyphens, as in `plan-themes.md`. When a file with that name already exists, update
  it; do not create a second plan for the same feature.
- **Location.** The repository root, or the working directory outside a git repository.
- **Shape.** Read `${CLAUDE_SKILL_DIR}/assets/plan-template.md` before writing. The plan has exactly the
  template's sections, in the template's order, and follows the instructions in its "How to use this template"
  comment. Do not copy that comment into the plan. Keep the `<!-- References -->` marker.
- **Reply.** After writing the file, reply with its path.
