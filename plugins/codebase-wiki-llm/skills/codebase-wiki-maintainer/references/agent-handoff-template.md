<!-- Generated from codebase/references/agent-handoff-template.md. Do not edit directly. -->

# Agent Handoff Template

Use this template for the `handoff` page (Core map). It is a pass-the-baton document,
not a narrative session summary.

```markdown
---
title: Agent Handoff
updated: YYYY-MM-DD
sources:
  - <wiki-root>/SCHEMA.md
  - <wiki-root>/<Core map log path>
  - <wiki-root>/<Core map tracker path>
  - <source-path>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Agent Handoff

## Current Work State
<!-- wiki:state -->

- Tracker IDs: <IDs for current work, or none; status is in the mapped tracker>
- Goal: <current objective>
- Last completed step: <evidence-backed step, or Not verified - <reason>>
- Current branch: `<branch or unknown>`
- Last commit: `<short-sha or unknown>`
- Worktree: <clean | dirty | unknown>

## Baton For Next Coding Agent
<!-- wiki:baton -->

| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
| 1 | T1 - <next step> | `<file>`, `<file>` | <observable completion criterion> | `<command>` | <risk/blocker/unknown> |

## Blockers
<!-- wiki:blockers -->

| Blocker | Type | Needed from | Current workaround |
| --- | --- | --- | --- |
| <blocker or none> | external | <person/system/unknown> | <workaround or none> |

## Known Risks
<!-- wiki:risks -->

| Risk | Impact | Mitigation | Evidence |
| --- | --- | --- | --- |
| <risk> | <impact> | <mitigation> | <source/page> |

## Commands Already Run
<!-- wiki:commands-run -->

| Command | Directory | Result | Evidence / notes |
| --- | --- | --- | --- |
| `<command>` | `<path>` | pass @<short-sha> | <brief result> |

## Do Not Redo
<!-- wiki:do-not-redo -->

- <work already completed and where it is recorded>

## Evidence Trail
<!-- wiki:evidence-trail -->

- `log` page: latest entries (SCHEMA `## Log format`, author human or agent)
- `tracker` page: IDs of the open work
- `decisions` folder: the decision files that apply
```

Rules:

- `Tracker IDs` references the mapped tracker; do not duplicate activity
  status here. Git state and verified steps remain in the handoff.
- Resolve source placeholders to concrete repository-relative paths before
  writing; use the confirmed wiki root and Core map paths.
- Every task in `Baton For Next Coding Agent` needs start files, done criteria,
  and a verification command. If verification is impossible, write
  `Not verified - <reason>`.
- Each baton task starts with its tracker ID (`T12 - <next step>`); `Done when`
  may point to the tracker (`see T12`) instead of repeating the criteria.
- When no work is left, write the line `No open work.` under the baton heading
  instead of the table; never invent tasks.
- Write headings in the SCHEMA language; keep each `<!-- wiki:... -->` marker
  on the line under its heading.
- Include git state when git is available. If unavailable, write `unknown`.
- Keep it current when plans, next tasks, blockers, architecture decisions, or
  meaningful verification results change.
- Do not repeat a long narrative; link to the `log` page for chronology.
