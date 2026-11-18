---
type: Project
title: Work Tracker
description: Status of open work and next steps for the plugin.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - wiki/log.md
  - wiki/agent/handoff.md
  - docs/release-checklist.md
source_commit: 94f5dc0
confidence: high
---
# Work Tracker

Only source of status. IDs (`T1`, `T2`, …) are stable and never reused. Other
pages cite IDs without repeating their status. Status icons: see SCHEMA.md
`## Conventions`. External issues and PRs are linked, never copied as status.

## Next steps
<!-- wiki:next -->

**In one line:** 0.16.0 is implemented on `dev` and waits for release notes and the go-ahead (2026-11-18).

1. Finish release notes and publish 0.16.0 (T1)
2. T2 - waits for T1

## Open
<!-- wiki:open -->

| ID | Status | Goal | Done when | Owner | Next verification | Evidence | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | 🟡 | Release plugin 0.16.0 (budgets, whole-word private terms, legacy rules on demand, `\uXXXX` in hooks, this wiki) | suite green; CHANGELOG and checklist written; `main`, `dev` and tag `v0.16.0` pushed | Stefano (asked 2026-11-18) | `bash scripts/run-tests.sh`; `git ls-remote origin` | [plan](../../docs/superpowers/plans/2026-11-18-release-0.16.0.md) | — |
| T2 | ⚪ | Desktop app aligned with plugin 0.16.0: whole-word terms, budget fallbacks, bundled validator, field-test references removed | app tests and build pass; app checker exit 0 | Stefano (asked 2026-11-18, deferred until the plugin ships) | `cargo test --workspace && npm test` | [plan Task 7](../../docs/superpowers/plans/2026-11-18-release-0.16.0.md) | T1 |

## Proposals
<!-- wiki:proposals -->

Ideas and suggested work nobody approved yet: no ID, no status icon.

| Proposal | By | Date | Why |
| --- | --- | --- | --- |
| Real-host trial of 0.16.0 on Codex, Claude Code and Antigravity | agent | 2026-11-18 | open item in every release checklist since 0.9.1 |
| Reinstall the Antigravity plugin with `agy plugin install` after the push | agent | 2026-11-18 | Antigravity copies the plugin at install time |

## Done
<!-- wiki:done -->

| ID | Status | Goal | Closed | Criteria met | Evidence |
| --- | --- | --- | --- | --- | --- |
