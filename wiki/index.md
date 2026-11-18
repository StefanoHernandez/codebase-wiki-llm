---
title: Codebase Wiki LLM wiki
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - wiki/SCHEMA.md
  - wiki/project/work-tracker.md
  - CHANGELOG.md
source_commit: 94f5dc0
confidence: high
---
# Codebase Wiki LLM wiki

The plugin that keeps an engineering wiki inside a software repository, for
Codex, Claude Code and Antigravity. This wiki describes the plugin itself and
is maintained with its own commands.

## Index

### Project
- [Work tracker](project/work-tracker.md) — status of open work and next steps
- [Log](log.md) — what was done, when, with evidence
- [Decisions](project/decisions/) — format version, SecondBrain removal, validator JSON, budgets, public wiki
- [Risks](project/risks.md) — what can break a release or a user's wiki

### Architecture
- [Architecture](architecture.md) — canonical sources, generated packages, validator, hooks

### Cross-cutting
- [Schema](SCHEMA.md) · [agent context](agent/context.md) · [handoff](agent/handoff.md)
- [Troubleshooting](troubleshooting.md) · [glossary](glossary.md)
- Release history: [CHANGELOG](../CHANGELOG.md) · [release checklist](../docs/release-checklist.md)

## Where things stand

Status lives only in the [tracker](project/work-tracker.md), with the next
steps; what was done and when in the [log](log.md).

## How this wiki is organised
<!-- wiki:owners -->

| Topic | Owner page |
| --- | --- |
| Activity status, next steps | [tracker](project/work-tracker.md) |
| What was done, when | [log](log.md) |
| Decisions and why | [decisions](project/decisions/) |
| Risks | [risks](project/risks.md) |
| Next task for an agent | [handoff](agent/handoff.md) |
| Verified facts | [agent context](agent/context.md) |
| How the plugin is built | [architecture](architecture.md) |
| Release history | [CHANGELOG](../CHANGELOG.md) |
