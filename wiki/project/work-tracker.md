---
type: Project
title: Work Tracker
description: Status of open work and next steps for the plugin.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:23:35Z }
sources:
  - wiki/log.md
  - wiki/agent/handoff.md
  - docs/release-checklist.md
source_commit: eef6bfa
confidence: high
---
# Work Tracker

Only source of status. IDs (`T1`, `T2`, …) are stable and never reused. Other
pages cite IDs without repeating their status. Status icons: see SCHEMA.md
`## Conventions`. External issues and PRs are linked, never copied as status.

## Next steps
<!-- wiki:next -->

**In one line:** 0.16.0 is published (2026-11-18); the desktop app is next.

1. Align the desktop app with 0.16.0 (T2)

## Open
<!-- wiki:open -->

| ID | Status | Goal | Done when | Owner | Next verification | Evidence | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |
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
| T1 | 🟢 | Release plugin 0.16.0 | 2026-11-18 | suite green; CHANGELOG and checklist written; `main`, `dev` and `v0.16.0` pushed at `eef6bfa` | [CI run](https://github.com/StefanoHernandez/codebase-wiki-llm/actions/runs/44302892992); `git ls-remote origin`; [checklist](../../docs/release-checklist.md) |
