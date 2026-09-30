# Decision Template

One decision per file in the `decisions` role folder (Core map), named
`NNNN-<slug>.md` with a four-digit, never-reused number.

````markdown
---
title: NNNN - <decision>
updated: YYYY-MM-DD
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

- Agents write decisions as `proposed`. A decision becomes `accepted` only
  with an explicit human choice or an approval documented in the project's
  process, recorded under `## Approval`.
- Code shows what was built, not why: reasons nobody recorded are written
  `Reasons not recorded.`, never inferred.
- A rejected or superseded decision stays; its status says why it no longer
  applies.
