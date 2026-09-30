# Work Tracker Template

Use this template for the `tracker` page (Core map). It connects project state
to agent handoff tasks.

```markdown
---
title: Work Tracker
updated: YYYY-MM-DD
sources:
  - <wiki-root>/log.md
  - <wiki-root>/agent/handoff.md
  - <source-files-or-plans>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Work Tracker

Only source of status. IDs (`T1`, `T2`, …) are stable and never reused. Other
pages cite IDs without repeating their status. Status icons: see SCHEMA.md
`## Conventions`.

## Open

| ID | Status | Activity | Phase | Owner | Next verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | 🟡 | <activity> | <phase/release/sprint or -> | human/agent | `<command>` | <link or `⚠️ NOT VERIFIED`> |

## Done

| ID | Activity | Closed | Evidence |
| --- | --- | --- | --- |
```

Rules:

- Keep this page compact; detail belongs in topic pages and the log.
- Link open work to the `handoff` page when another coding agent needs to
  continue it.
