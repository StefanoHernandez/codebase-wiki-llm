---
title: Wiki Schema
updated: 2026-10-02
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
`log-archive` reserves a directory created on the first archive write; an
empty archive directory is not required at init or adoption.

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
- Status: 🟢 done and verified · ⚫ closed by a person without proven criteria
  · 🟡 in progress · ⚪ to do · 🔴 blocked.
  🔴 means "work stopped", not "serious". A page that uses the icons for
  something else (e.g. risk severity) says so at the top.
- Terminal tracker rows carry `Status`: 🟢 requires every `Done when`
  criterion to be proven; ⚫ requires explicit human closure recorded as
  `closed by <person> YYYY-MM-DD; not proven: <what>` in `Criteria met`,
  with the closure source in `Evidence`. Never infer closure authority.
  Legacy Done rows without `Status` remain valid when their criteria are proven.
- Dates: `YYYY-MM-DD`.
- The `tracker` is the only source of status; external tools are linked, never copied as status.
- Language: headings and prose use the Project profile language. Fixed tokens
  never change: section markers `<!-- wiki:<id> -->`, Core map role names,
  frontmatter keys, `⚠️ NOT VERIFIED`, `⚠️ TO RE-VERIFY`,
  `Not verified - <reason>`, `No open work.`, status icons, ID prefixes.
- Section markers: sections that tools check carry their marker on the line
  right under the heading (context, handoff and tracker templates). Translate
  the heading, keep the marker.
- Page metadata: new and substantively updated pages require frontmatter
  with `title`, `updated`, actual supporting `sources`, `source_commit`, and
  `confidence`. During gradual adoption, untouched legacy pages and
  marker-only edits retain explicit metadata gaps. Structural adoption does
  not certify them; validation stays incomplete until the gaps are resolved.
  An unknown reviewed source baseline is `source_commit: unknown`; metadata
  dates and current commits never establish verification of old prose.

## Evidence

Evidence is proportional to the claim:

| Claim | Evidence |
| --- | --- |
| Verification (test, build, command result) | command, essential output, date, code state |
| Description (files, structure, relations, behavior read from code) | the precise source: a file in `sources:` or inline, with symbol or line when useful |
| Decision | accepted: who approved it, where (message, PR, meeting note) and when; proposed: who proposed it and when; reasons nobody recorded are written as unknown |
| Risk | the stated assumption and what would trigger it |

Code state is `@<short-sha>`, plus `+local` when uncommitted changes to the
relevant files were part of the result; add branch or environment when they
affect the result; without git write `code state unknown`.
For log entries, an explicit local `## Log format` rule may require a
different representation, such as code state not recorded by project policy.
Preserve the actual verification evidence and state the limit on identifying
its code baseline.

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

These are defaults. Keep an explicit existing project log convention during
adoption and record it here, including a ban on commit hashes when present.
When hashes cannot be recorded, retain commands, essential output, dates and
relevant environment; mark code state as not recorded by project policy.
This log restriction does not automatically apply to page `source_commit`.
Sync validates every Git anchor before using it; with no usable log baseline,
it reports incomplete committed-change coverage rather than `nothing to do`.

```markdown
## YYYY-MM-DD · <title> · human | agent
- What: <what was done>
- Evidence: `<command>` → <essential output> @<short-sha>[+local]   (or `> ⚠️ NOT VERIFIED - <reason>`)
- IDs: T12, T13
```

When a phase of the project division closes, `/wiki-sync` moves that phase's
entries to `<phase>.md` under the `log-archive` path; when the log exceeds its
budget, it moves whole months, oldest first, to `<YYYY-MM>.md`, always keeping
the last 10 entries. It does this without asking, keeps one link line per
archive in the log, and reports the move.

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
- `/wiki-sync`: do not ask, except unresolved Step 7 proposals; document an
  already approved decision as `accepted` with its recorded authority without
  asking again; archive the log by the `## Log format` rule without asking;
  run only for small source changes.
- `/wiki-lint`: do not ask; produce a read-only report.

## What this repo is about

Replace this section during `/wiki-init` with one concise paragraph describing
the repository.
