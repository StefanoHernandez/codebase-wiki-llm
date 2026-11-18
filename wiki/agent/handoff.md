---
type: AgentNote
title: Agent Handoff
description: Where the 0.16.0 release stands and what to do next.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - wiki/SCHEMA.md
  - wiki/log.md
  - wiki/project/work-tracker.md
  - docs/release-checklist.md
source_commit: 94f5dc0
confidence: high
---
# Agent Handoff

## Current Work State
<!-- wiki:state -->

- Tracker IDs: T1, T2
- Goal: release plugin 0.16.0, then align the desktop app
- Last completed step: legacy rules moved to `references/legacy-adoption.md`; suite green @94f5dc0
- Current branch: `dev`
- Last commit: `94f5dc0`
- Worktree: clean

## Baton For Next Coding Agent
<!-- wiki:baton -->

| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
| 1 | T1 - finish the 0.16.0 release notes and get the go-ahead to push | `CHANGELOG.md`, `docs/release-checklist.md` | see T1 | `bash scripts/run-tests.sh` | push and tag only with Stefano's OK |
| 2 | T2 - waits for T1 | `docs/superpowers/plans/2026-11-18-release-0.16.0.md` (Task 7) | see T2 | `cargo test --workspace && npm test` in the app repo | app changes deferred by Stefano |

## Blockers
<!-- wiki:blockers -->

| Blocker | Type | Needed from | Current workaround |
| --- | --- | --- | --- |
| Go-ahead to push and tag 0.16.0 | human | Stefano | work stays on local `dev` |

## Known Risks
<!-- wiki:risks -->

| Risk | Impact | Mitigation | Evidence |
| --- | --- | --- | --- |
| See the register | — | — | [risks](../project/risks.md) |

## Commands Already Run
<!-- wiki:commands-run -->

| Command | Directory | Result | Evidence / notes |
| --- | --- | --- | --- |
| `bash scripts/run-tests.sh` | repo root | pass @94f5dc0 | exit 0 |

## Do Not Redo
<!-- wiki:do-not-redo -->

- Field-test references replaced with generic wording in current files ([log](../log.md)); history is deliberately not rewritten ([decision 0005](../project/decisions/0005-public-wiki-and-private-terms.md)).

## Evidence Trail
<!-- wiki:evidence-trail -->

- `log` page: latest entries
- `tracker` page: T1, T2
- `decisions` folder: 0004, 0005
