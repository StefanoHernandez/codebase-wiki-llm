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
<!-- wiki:goals -->
- Goal: <one line per outcome the project must deliver>
- Non-goal: <what we are explicitly NOT doing; this stops agents over-building>

## Non-Negotiable Rules
<!-- wiki:rules -->
1. <rule that must never be broken, with the reason in a few words>

## Frequent Commands
<!-- wiki:commands -->
| Purpose | Command | Verified |
| --- | --- | --- |
| Test | `<command>` | YYYY-MM-DD @<short-sha> or `⚠️ NOT VERIFIED - <reason>` |

## Verified Facts
<!-- wiki:verified-facts -->
Do not re-derive these. Re-check a fact only when its evidence changed or it is
marked `⚠️ TO RE-VERIFY`.

| Fact | Value | Evidence | Verified |
| --- | --- | --- | --- |
| <fact> | <value> | `<command>` or <document> | YYYY-MM-DD @<short-sha> |

**Errors already corrected, do not reintroduce:** <wrong belief> → <correct fact>.

## Read First
<!-- wiki:read-first -->
1. <at most five links: index, tracker, handoff (its baton row 1 is the first task to pick up), the page for the current work>
```

Rules:

- Do not write a generic project summary. Every fact needs evidence.
- Write headings in the SCHEMA language; keep each `<!-- wiki:... -->` marker on
  the line under its heading.
- Mark unverified commands and facts `⚠️ NOT VERIFIED - <reason>`.
- Keep implementation detail out unless it helps a new coding agent decide
  where to start.
- `/wiki-sync` updates a fact directly when new evidence proves it. When a
  fact's evidence changed and it cannot be re-proved, its Verified cell becomes
  `⚠️ TO RE-VERIFY (<what changed>)`; the row is never deleted silently.
