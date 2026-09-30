---
name: codebase-wiki-maintainer
description: Knowledge for maintaining an engineering-first software project wiki (wiki/ by default, or the folder named in .wikidir).
---

<!-- Generated from codebase/maintainer.md. Do not edit directly. -->

# Wiki Maintainer

This skill maintains the wiki under `<wiki-root>/`. It keeps shared context
between the people and the agents working on this repository, a log of what
was done with its evidence, and the decisions taken and why. Everything else is
an optional topic.

Everything is written for fast, source-grounded answers to: where do I change
this, what must not break, how do I verify it, why is it shaped this way, and
what is the current state.

## Wiki root

In these instructions, `<wiki-root>` is this repository's wiki directory,
relative to the repository root (`wiki` by default). Resolve it once, before
anything else, use the resolved value in every wiki path, and state it:
`Wiki root: <value>/`.

1. If your context contains a line `Codebase Wiki LLM: wiki_root: <value>`
   (added when the session started) and you have not created or changed the
   wiki root during this session, use `<value>`.
2. Otherwise, if `.wikidir` exists at the repository root, read that file
   directly: its first non-empty line is the folder name. Do not look for it
   with a file search: searches skip hidden and gitignored files.
3. Otherwise, if `wiki/SCHEMA.md` exists, `<wiki-root>` is `wiki`.
4. Otherwise the repository has no wiki yet.

The value must be a single directory name matching
`^\.?[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9_-])?$` (no trailing dot) and must
not be one of `.git`, `.github`, `.claude`, `.codex`, `.agents`, `.agent`,
`.gemini`, `.opencode`, `.obsidian`, `.vscode`, `node_modules`, `.wikidir`,
compared case-insensitively. If it breaks these rules or names a directory
that does not exist, stop and tell the user without guessing another location.

## Truth hierarchy

When sources disagree, use this order:

1. Source code, tests, configs, CI, runtime manifests, command output.
2. Topic pages (SCHEMA `## Topics`).
3. `tracker`, `decisions`, `risks` (Core map).
4. `context`, `handoff`, `log`.

A page must not contradict a higher level; fix the lower page.

## Core and topics

This wiki keeps shared context between the people and the agents working on
this repository, a log of what was done with its evidence, and the decisions
taken and why. Everything else is an optional topic.

- `<wiki-root>/SCHEMA.md` holds the repo conventions; read it before any wiki
  operation. Its `## Core map` is the only way to locate core pages (index,
  log, tracker, decisions, risks, context, handoff, troubleshooting,
  glossary): never assume a path.
- Topics are listed in SCHEMA `## Topics`. The user can ask to add one at any
  time: create the page and add a row.
- The single log replaces `agent/activity.md`. Entries follow SCHEMA
  `## Log format`.
- Decisions are one file each; see `references/decision-template.md`.
- Troubleshooting entries follow `references/troubleshooting-template.md`.
- Context, handoff and tracker follow `references/agent-context-template.md`,
  `references/agent-handoff-template.md` and
  `references/work-tracker-template.md`.

## Page conventions

Every wiki page must have YAML frontmatter:

```yaml
---
title: Short descriptive title
updated: 2026-05-19
sources:
  - src/routes/nodes.ts
  - tests/routes/nodes.test.ts
source_commit: abc123
confidence: high
---
```

Rules:

- `sources:` must name concrete evidence files.
- `source_commit:` is the current short git commit when git is available.
- `confidence:` is `high`, `medium`, or `low`.
- Use standard relative markdown links. Do not use `[[wikilink]]` syntax.
- Prefer tables for file maps, commands, config, APIs, risks, and requirements.
- Prefer Mermaid for flows, module relationships, and state machines.
- Every write follows SCHEMA `## Evidence`; log entries follow SCHEMA
  `## Log format`.

## Engineering quality bar

Topic pages must help someone work safely. A module page (optional `modules` topic) should include,
when evidence exists:

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

Keep claims concrete. Prefer "run `npm test` from `ui/builder`" over "run the
tests". If no reliable verification exists, say that explicitly.

## Confidence and decay

- **high**: written from current evidence and no commits touched the listed
  sources since `source_commit`.
- **medium**: one to four commits touched listed sources, or the page includes
  limited interpretation beyond direct evidence.
- **low**: five or more commits touched listed sources, listed sources are
  missing, or key claims cannot be verified.

Lower confidence during sync or lint when evidence ages. Never silently delete
old claims; correct them with a supersession note when useful.

## Operations

### Init

Bootstrap a repo-local wiki. Survey the repository, propose scope, ask once for
approval, then create a small but useful wiki.

### Ingest

Deep-dive into a file, directory, feature, or topic. Update the topic page and
any affected core pages.

### Sync

Small, surgical update after source changes. Update only affected existing wiki
pages. If the change needs new pages or broad reorganization, recommend ingest.

### Lint

Read-only health report. Check staleness, drift, orphans, gaps,
contradictions, unsupported claims, frontmatter, and legacy docs. Do not modify the wiki during lint unless the
user explicitly asks to save a report.

## Non-negotiable rules

1. Do not invent. If you cannot verify a claim, omit it or mark it as a gap.
2. Cite concrete evidence in `sources:`.
3. Higher levels of the truth hierarchy outrank lower pages.
4. Keep pages short enough to be useful. Split pages that grow past roughly 200
   lines.
5. Never modify source files during wiki operations.
6. Propose deletion or retirement; do not silently delete pages or legacy docs.
7. Update the `index` page whenever pages are added, renamed, or removed.
8. Append to the `log` after init, ingest, and sync. Lint is read-only by default.
9. Respect `<wiki-root>/SCHEMA.md` over these defaults.
10. Keep agent context and handoff evidence-based; mark what is unverified
    `> ⚠️ NOT VERIFIED`.
11. Each handoff task must include start files, done criteria, and a
    verification command or an explicit `Not verified - <reason>`.
12. Never write a term from `.private-terms` into any file other than
    `.private-terms`.
13. Files outside `<wiki-root>/` are changed only by `/wiki-init` steps the user
    confirmed (`.wikidir`, `.gitignore`, the agent entry file,
    `.git/hooks/pre-commit`).
