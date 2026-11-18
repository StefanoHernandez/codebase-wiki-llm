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

**In one line:** 0.16.0 is published and the desktop app 0.7.7 follows it (2026-11-18); no open work.

1. Pick from Proposals (real-host trial, Antigravity reinstall)

## Open
<!-- wiki:open -->

| ID | Status | Goal | Done when | Owner | Next verification | Evidence | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- |

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
| T2 | 🟢 | Desktop app aligned with plugin 0.16.0: whole-word terms, budget fallbacks, bundled validator, field-test references removed | 2026-11-18 | app tests and tag CI green; app checker exit 0; app 0.7.7 published as latest | [app release v0.7.7](https://github.com/StefanoHernandez/codebase-wiki-app/releases/tag/v0.7.7); app CI run 44315200732 |
