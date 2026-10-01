# Decision Template

One decision per file in the `decisions` role folder (Core map), named
`NNNN-<slug>.md` with a four-digit, never-reused number.

````markdown
---
title: NNNN - <decision>
updated: YYYY-MM-DD
sources:
  - <source-path>
source_commit: <short-sha-or-unknown>
status: proposed | accepted | rejected | superseded by NNNN
confidence: high | medium | low
---

# NNNN - <decision>

## Context
<the problem and the constraints, with links to evidence>

## Decision
<what we chose, in one or two sentences>

## Alternatives rejected
- <alternative>: <why not>

## Consequences
<what this makes easier, harder, or forbidden; related IDs>

## Approval
<accepted: who approved it, where (message, PR review, meeting note) and when.
proposed: who proposed it and when.>
````

Rules:

- Record an already approved decision directly as `accepted` with who
  approved it, where and when under `## Approval`; no repeat permission is
  needed to document existing approval. Acceptance requires an explicit human
  choice or approval documented in the project's process; never infer it from
  code, silence or an agent suggestion.
- New unresolved ideas remain `proposed`, with who proposed them and when.
  Ask for a choice only when it is unresolved.
- Resolve `<source-path>` to a concrete repository-relative evidence path
  before writing. Cite actual source files or recorded approval documents;
  conversational authority is identified under `## Approval`.
- Code shows what was built, not why: reasons nobody recorded are written
  `Reasons not recorded.`, never inferred. Do not invent rejected alternatives;
  if none were recorded, write `Alternatives not recorded.`.
- A rejected or superseded decision stays; its status says why it no longer
  applies.
- A decision accepted before this template may say `Approval not recorded.`
  under `## Approval`.
