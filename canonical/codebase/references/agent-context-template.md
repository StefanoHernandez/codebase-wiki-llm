# Agent Context Template

Use this template for `<wiki-root>/agent/context.md`. Keep it concise enough that a new
coding agent can read it before searching the codebase.

```markdown
---
title: Agent Context
updated: YYYY-MM-DD
sources:
  - README.md
  - <wiki-root>/index.md
  - <wiki-root>/engineering/architecture.md
  - <wiki-root>/engineering/development.md
  - <wiki-root>/engineering/testing.md
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Agent Context

## Project Snapshot

- Project: <name>
- Purpose: <one or two evidence-backed sentences>
- Current status: <active | maintenance | paused | unknown>
- Primary languages/frameworks: <list or unknown>
- Main runtime/deploy target: <value or unknown>

## Architecture At A Glance

| Area | Purpose | Start here |
| --- | --- | --- |
| <area> | <what it owns> | [page](../engineering/architecture.md) |

## Non-Negotiable Technical Rules

- <invariant/rule> - Source: <file/page>
- Unknown rules: Not verified.

## Core Commands

| Task | Command | Working directory | Evidence |
| --- | --- | --- | --- |
| Setup | `<command or unknown>` | `<path>` | `<source>` |
| Test | `<command or unknown>` | `<path>` | `<source>` |
| Lint | `<command or unknown>` | `<path>` | `<source>` |
| Build | `<command or unknown>` | `<path>` | `<source>` |

## Read First

1. [Master index](../index.md)
2. [Architecture](../engineering/architecture.md)
3. [Development](../engineering/development.md)
4. [Testing](../engineering/testing.md)
5. [Current handoff](handoff.md)

## Risks And Invariants

| Risk / invariant | Why it matters | Evidence |
| --- | --- | --- |
| <risk> | <impact> | <source/page> |

## High-Value Links

- [Project status](../project/status.md)
- [Work tracker](../project/work-tracker.md)
- [Decisions](../project/decisions.md)
- [Change map](../engineering/change-map.md)
```

Rules:

- Do not write a generic project summary. Every important claim needs a source.
- Use `unknown`, `pending`, or `Not verified.` when commands, status, or risks
  are not evidenced.
- Keep implementation detail out unless it helps a new coding agent decide
  where to start.
