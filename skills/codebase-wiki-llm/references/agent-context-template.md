<!-- Generated from codebase/references/agent-context-template.md. Do not edit directly. -->

# Agent Context Template

Use this template for the `context` page (Core map). Keep it concise enough
that a new coding agent can read it before searching the codebase.

```markdown
---
title: Agent Context
updated: YYYY-MM-DD
sources:
  - README.md
  - <wiki-root>/<Core map index path>
  - <wiki-root>/SCHEMA.md
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Agent Context

## Goals And Non-Goals
- Goal: <one line per outcome the project must deliver>
- Non-goal: <what we are explicitly NOT doing; this stops agents over-building>

## Non-Negotiable Rules
1. <rule that must never be broken, with the reason in a few words>

## Frequent Commands
| Purpose | Command | Verified |
| --- | --- | --- |
| Test | `<command>` | YYYY-MM-DD or `⚠️ NOT VERIFIED` |

## Verified Facts
Do not re-derive these. Re-check a fact only when its evidence changed.

| Fact | Value | Evidence | Verified |
| --- | --- | --- | --- |
| <fact> | <value> | `<command>` or <document> | YYYY-MM-DD |

**Errors already corrected, do not reintroduce:** <wrong belief> → <correct fact>.

## Read First
1. <at most five links: index, tracker, handoff, the page for the current work>
```

Rules:

- Do not write a generic project summary. Every fact needs evidence.
- Mark unverified commands and facts `⚠️ NOT VERIFIED`.
- Keep implementation detail out unless it helps a new coding agent decide
  where to start.
