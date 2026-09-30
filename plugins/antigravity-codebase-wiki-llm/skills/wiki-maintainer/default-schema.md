---
title: Wiki Schema
updated: 2026-05-19
confidence: high
---

<!-- Generated from codebase/default-schema.md. Do not edit directly. -->

# Wiki Schema for This Repo

This file is the repo-specific constitution for the wiki. Edit it when the
repository needs different conventions. Wiki workflows must read this file
before editing wiki content.

## Mission

This wiki keeps shared context between the people and the agents working on
this repository, a log of what was done with its evidence, and the decisions
taken and why. Everything else is an optional topic listed in `## Topics`.

## Truth hierarchy

1. Source code, tests, configs, CI, runtime manifests, command output.
2. Topic pages (`## Topics`).
3. `tracker`, `decisions`, `risks` (Core map).
4. `context`, `handoff`, `log`.

A page must not contradict a higher level. When it does, fix the lower page.

## Project profile

| Setting | Value |
| --- | --- |
| Language | English |
| Project division | none (phases/WP · releases · sprints/milestones · none) |
| Sensitive data | no |
| Agent entry file | none (CLAUDE.md · AGENTS.md · none) |

## Core map

Every workflow finds the core pages through this table. Paths are relative to
the wiki root. Change a path here to relocate a page.

| Role | Path |
| --- | --- |
| index | `index.md` |
| log | `log.md` |
| log-archive | `log/` |
| tracker | `project/work-tracker.md` |
| decisions | `project/decisions/` |
| risks | `project/risks.md` |
| context | `agent/context.md` |
| handoff | `agent/handoff.md` |
| troubleshooting | `troubleshooting.md` |
| glossary | `glossary.md` |

## Conventions

- Activity IDs: prefix `T`, stable, never reused; status lives only in the
  tracker.
- Status: 🟢 done and verified · 🟡 in progress · ⚪ to do · 🔴 blocked.
  🔴 means "work stopped", not "serious". A page that uses the icons for
  something else (e.g. risk severity) says so at the top.
- Dates: `YYYY-MM-DD`.

## Evidence

A technical claim carries the command that supports it, its essential output,
and the date. What is expected but not verified is marked
`> ⚠️ NOT VERIFIED`. Never write invented output "by way of example" next to
real output.

## Confidentiality

Off by default. When `Sensitive data` is `yes`:

- forbidden terms are listed one per line in `<wiki-root>/.private-terms`,
  which is git-ignored and never committed; this page records only the
  generic wording to use instead (e.g. "the partner");
- local-only paths must be git-ignored (`git check-ignore -v <path>`): in
  `.gitignore`, or in `.git/info/exclude` (never committed) when the path's
  name contains a forbidden term; the table below describes each with generic
  wording, never the path itself when its name holds a term;
- the pre-commit hook in `$(git rev-parse --git-path hooks)` runs the
  maintainer skill's `scripts/check-private-terms.sh` (or calls it with
  `sh "$(git rev-parse --git-path hooks)/check-private-terms.sh" || exit 1`);
  with `core.hooksPath` set, the user's hook manager runs that call line;
- the check covers file contents and tracked file names; binary files are
  skipped (`git grep -I`).

| Local-only path (generic wording) | Why |
| --- | --- |

## Budgets

| Budget | Default |
| --- | --- |
| Single page | 20 KB |
| Core read at a new context (agent entry file, SCHEMA, index, context, handoff, tracker, risks, troubleshooting, glossary, last 10 log entries) | 60 KB |
| log | 30 KB |

## Log format

```markdown
## YYYY-MM-DD · <title> · human | agent
- What: <what was done>
- Evidence: `<command>` → <essential output>   (or `> ⚠️ NOT VERIFIED`)
- IDs: T12, T13
```

When a phase of the project division closes, or the log exceeds its budget,
entries up to that date move to `<phase-or-period>.md` under the `log-archive` path and the
log keeps one link line per archive.

## Topics

| Topic | Path | What belongs there |
| --- | --- | --- |
| architecture | `architecture.md` | components, boundaries, data/control flow, invariants |

## Page granularity

- One page per coherent topic or code area; split a page that nears its budget.
- Keep the tracker the only place where status lives; other pages cite IDs.
- Keep `context` and `handoff` short and useful for the next session.

## Module page template (optional `modules` topic)

Use these sections when evidence exists:

```markdown
## Purpose
## Key files
## Public interface
## Data/control flow
## Invariants
## How to change this safely
## Verification
## Common failure modes
## Dependencies
## Related tests
## Open risks
```

## Decay policy

- Fast decay: topic pages.
- Medium decay: `tracker`, `risks`, `handoff`, `log`.
- Slow decay: `decisions`, `glossary`, `context`.

Lint should flag pages as low confidence when five or more commits touched their
listed sources since `source_commit`, when sources are missing, or when claims
are unsupported.

## Legacy docs

If these root-level docs exist and their content is absorbed into the wiki, lint
may propose retirement:

- `context_map.md`
- `project_status.md`
- `BUILD_PHASES.md`
- `ARCHITECTURE.md`
- `ROADMAP.md`
- `CHANGELOG.md` if it duplicates the `log`

Never delete automatically.

## Style preferences

- Use markdown tables for file maps, commands, APIs, config, risks,
  requirements, and claim support.
- Use Mermaid for flows, module graphs, state machines, and architecture maps.
- Use standard relative markdown links.
- Dates use ISO format (`YYYY-MM-DD`).
- Headings use sentence case.

## Question policy

- `/wiki-init`: ask once to confirm scope before writing.
- `/wiki-ingest` without a target: ask what to ingest.
- `/wiki-sync`: do not ask, except Step 7 proposals; run only for small source changes.
- `/wiki-lint`: do not ask; produce a read-only report.

## What this repo is about

Replace this section during `/wiki-init` with one concise paragraph describing
the repository.
