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
Level 1 tells what the system does now, not what it should do: code can hold a bug.

## Project profile

| Setting | Value |
| --- | --- |
| Language | English (headings and prose; fixed tokens in Conventions) |
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
- The `tracker` is the only source of status; external tools are linked, never copied as status.
- Language: headings and prose use the Project profile language. Fixed tokens
  never change: section markers `<!-- wiki:<id> -->`, Core map role names,
  frontmatter keys, `⚠️ NOT VERIFIED`, `⚠️ TO RE-VERIFY`,
  `Not verified - <reason>`, `No open work.`, status icons, ID prefixes.
- Section markers: sections that tools check carry their marker on the line
  right under the heading (context, handoff and tracker templates). Translate
  the heading, keep the marker.

## Evidence

Evidence is proportional to the claim:

| Claim | Evidence |
| --- | --- |
| Verification (test, build, command result) | command, essential output, date, code state |
| Description (files, structure, relations, behavior read from code) | the precise source: a file in `sources:` or inline, with symbol or line when useful |
| Decision | who approved it, where (message, PR, meeting note) and when; reasons nobody recorded are written as unknown |
| Risk | the stated assumption and what would trigger it |

Code state is `@<short-sha>`, plus `+local` when uncommitted changes to the
relevant files were part of the result; add branch or environment when they
affect the result; without git write `code state unknown`.

What cannot be checked (missing tests, unreachable service, access denied, no
git) is marked `> ⚠️ NOT VERIFIED - <reason>` on that conclusion only; the
rest of the work goes on. A check that could not run is neither a pass nor a
failure. Never write invented output "by way of example" next to real output.

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
- Evidence: `<command>` → <essential output> @<short-sha>[+local]   (or `> ⚠️ NOT VERIFIED - <reason>`)
- IDs: T12, T13
```

When a phase of the project division closes, or the log exceeds its budget,
`/wiki-sync` moves the entries up to that date to `<phase-or-period>.md` under
the `log-archive` path without asking, keeps one link line per archive in the
log, and reports the move.

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

Lint judges staleness by impact: a change to a listed source makes a page
stale when it can affect what the page says (an interface, contract, command,
config key or described behavior), not when it is cosmetic. Five or more
commits touching listed sources since `source_commit`, missing sources and
unsupported claims are signals to check.

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

- `/wiki-init`: ask once to confirm scope before writing; in adopt mode, also
  ask once for the migration plan.
- `/wiki-ingest` without a target: ask what to ingest.
- `/wiki-sync`: do not ask, except Step 7 proposals; archive the log by the
  `## Log format` rule without asking; run only for small source changes.
- `/wiki-lint`: do not ask; produce a read-only report.

## What this repo is about

Replace this section during `/wiki-init` with one concise paragraph describing
the repository.
