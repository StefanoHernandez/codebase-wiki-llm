# Agent Handoff Template

Use this template for `<wiki-root>/agent/handoff.md`. It is a pass-the-baton document,
not a narrative session summary.

```markdown
---
title: Agent Handoff
updated: YYYY-MM-DD
sources:
  - <wiki-root>/agent/activity.md
  - <wiki-root>/project/work-tracker.md
  - <changed-source-or-config-file>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Agent Handoff

## Current Work State

- Status: <not started | in progress | blocked | ready for review | done | unknown>
- Goal: <current objective>
- Last completed step: <evidence-backed step or Not verified.>
- Current branch: `<branch or unknown>`
- Last commit: `<short-sha or unknown>`
- Worktree: <clean | dirty | unknown>

## Baton For Next Coding Agent

| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
| 1 | <next task> | `<file>`, `<file>` | <observable completion criterion> | `<command>` | <risk/blocker/unknown> |

## Blockers

| Blocker | Type | Needed from | Current workaround |
| --- | --- | --- | --- |
| <blocker or none> | external | <person/system/unknown> | <workaround or none> |

## Known Risks

| Risk | Impact | Mitigation | Evidence |
| --- | --- | --- | --- |
| <risk> | <impact> | <mitigation> | <source/page> |

## Commands Already Run

| Command | Directory | Result | Evidence / notes |
| --- | --- | --- | --- |
| `<command>` | `<path>` | pass | <brief result> |

## Do Not Redo

- <work already completed and where it is recorded>

## Evidence Trail

- [Activity log](activity.md)
- [Work tracker](../project/work-tracker.md)
- [Project status](../project/status.md)
- [Decisions](../project/decisions.md)
```

Rules:

- Every task in `Baton For Next Coding Agent` needs start files, done criteria,
  and a verification command. If verification is impossible, write
  `Not verified - <reason>`.
- Include git state when git is available. If unavailable, write `unknown`.
- Keep it current when plans, next tasks, blockers, architecture decisions, or
  meaningful verification results change.
- Do not repeat a long narrative; link to `activity.md` for chronology.
