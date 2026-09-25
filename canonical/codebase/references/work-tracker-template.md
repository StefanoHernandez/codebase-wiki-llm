# Work Tracker Template

Use this template for `<wiki-root>/project/work-tracker.md`. It connects project state
to agent handoff tasks.

```markdown
---
title: Work Tracker
updated: YYYY-MM-DD
sources:
  - <wiki-root>/agent/activity.md
  - <wiki-root>/agent/handoff.md
  - <source-files-or-plans>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Work Tracker

## Active Work

| Priority | Work item | Status | Owner | Evidence | Next verification |
| --- | --- | --- | --- | --- | --- |
| P0 | <item> | in progress | <agent/user/unknown> | <source/page> | `<command>` |

## Planned Work

| Priority | Work item | Why it matters | Start files | Done when |
| --- | --- | --- | --- | --- |
| P1 | <item> | <reason> | `<file>` | <criterion> |

## Recently Completed

| Date | Work item | Verification | Evidence |
| --- | --- | --- | --- |
| YYYY-MM-DD | <item> | `<command>` | <source/page> |

## Blocked / Waiting

| Work item | Blocker | Needed from | Next check |
| --- | --- | --- | --- |
| <item> | <blocker> | <source/person/system> | <date or unknown> |
```

Rules:

- Keep this page compact; detailed implementation notes belong in
  `engineering/`, `modules/`, or `agent/activity.md`.
- Link active work to `agent/handoff.md` when another coding agent needs to
  continue it.
