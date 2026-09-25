---
name: wiki-maintainer
description: Knowledge for maintaining an engineering-first software project wiki (wiki/ by default, or the folder named in .wikidir).
---

<!-- Generated from codebase/maintainer.md. Do not edit directly. -->

# Wiki Maintainer

This skill maintains an engineering-first software project wiki under
`<wiki-root>/`. The wiki is durable project knowledge for software engineers,
project leads, future agents, and reusable project documentation.

The primary reader is an engineer who needs to change the software safely. The
secondary readers are project managers, reviewers, stakeholders, and future
agents. Optimize every page for fast, source-grounded answers to:

- where do I change this?
- what must not break?
- how do I verify the change?
- why is the system shaped this way?
- what is the current project state and risk?
- what claims can be reused in external documentation?

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

1. Source code, tests, migrations, configs, CI, and runtime manifests.
2. `<wiki-root>/engineering/` and `<wiki-root>/modules/`.
3. `<wiki-root>/project/`.
4. `<wiki-root>/project-docs/`.
5. `<wiki-root>/agent/` and historical logs.

`engineering/` and `modules/` are authoritative for technical reality.
`project/` summarizes delivery state and decisions. `project-docs/` reuses and
communicates supported claims; it must not invent capabilities.

## The three layers

1. **Raw sources** - code, tests, configs, docs, manifests, CI, issue exports,
   meeting notes, and proposal material. Read them as evidence. During wiki
   operations, do not modify files outside `<wiki-root>/`, except
   `.wikidir`, which `/wiki-init` writes.
2. **The wiki** - `<wiki-root>/`. The agent owns this knowledge layer and keeps
   it useful, accurate, and navigable.
3. **The schema** - `<wiki-root>/SCHEMA.md`. Repo-specific conventions override
   these defaults. Read it before any wiki operation.

## Default wiki structure

```text
<wiki-root>/
├── index.md
├── SCHEMA.md
├── log.md
├── overview.md
├── overview-<project-slug>.md
├── engineering/
│   ├── architecture.md
│   ├── data-model.md
│   ├── development.md
│   ├── testing.md
│   ├── operations.md
│   ├── troubleshooting.md
│   └── change-map.md
├── modules/
│   └── <module-or-area>.md
├── project/
│   ├── status.md
│   ├── work-tracker.md
│   ├── roadmap.md
│   ├── milestones.md
│   ├── risks.md
│   ├── requirements.md
│   └── decisions.md
├── project-docs/
│   ├── project-brief.md
│   ├── value-proposition.md
│   ├── use-cases.md
│   ├── audience.md
│   ├── impact.md
│   ├── evidence.md
│   ├── demo-materials.md
│   └── faq.md
├── agent/
│   ├── context.md
│   ├── activity.md
│   └── handoff.md
└── glossary.md
```

For small repositories, create the structure but keep unsupported pages as short
stubs with explicit "No verified content yet" notes. Do not fill project or
communication pages by guessing.

## Portable project overview

Every project wiki should include a portable overview file:

```text
<wiki-root>/overview-<project-slug>.md
```

The project slug must be lowercase kebab-case with no spaces, for example:

- `overview-securegraph-rag.md`
- `overview-popup.md`
- `overview-template-latex.md`

This file is the canonical short project card. It bridges the technical project
wiki and the user's general SecondBrain vault. It should let someone understand
the project in a few minutes without reading the whole technical wiki.

It must include:

- what the project is;
- why it exists;
- current status;
- main stack or technical areas;
- milestones or next steps;
- important decisions to remember;
- links to the most relevant technical wiki pages;
- `## Personal Wiki Export`.

`## Personal Wiki Export` is written for import into a personal/work
SecondBrain vault, usually under `raw/projects/` before ingestion. It should
include project name, short description, current status, role in the user's
work/life, personal motivation if known, technologies or skills represented,
important next steps, and long-term notes.

Do not invent personal motivation, career goals, subjective meaning, or user
priorities. If personal information is not known, write `Da confermare.`

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

## Engineering quality bar

Engineering pages must help someone work safely. A module page should include,
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

## Project layer

`<wiki-root>/project/` describes project management state: roadmap, milestones, risks,
requirements, and decisions. It should link to technical evidence rather than
duplicating technical details.

Risk entries should include impact, evidence, mitigation, owner if known, and
status. Decisions should include context, decision, rationale, consequences, and
links to affected engineering pages.

`project/work-tracker.md` tracks active, planned, completed, and blocked work.
It connects project status to agent handoff tasks. Keep it compact and
evidence-backed. Detailed implementation notes belong in `engineering/`,
`modules/`, or `agent/activity.md`.

## Project-docs layer

`<wiki-root>/project-docs/` stores reusable communication material for READMEs,
presentations, client documentation, grant/bid material, product notes, and
public explanations.

Communication claims must be supported. Use this pattern when useful:

```markdown
## Claim
The project reduces onboarding time on unfamiliar repositories.

## Supported by
- [change map](../engineering/change-map.md)
- [evidence](evidence.md)

## Reusable for
- README
- project brief
- presentation
- proposal
```

Do not let `project-docs/` become marketing fiction. If a claim is desirable
but unsupported, mark it as a gap or hypothesis.

## Agent layer

`<wiki-root>/agent/` replaces scattered project-context files. It records what agents
need to know and what they did.

- `context.md` - fast onboarding for future coding agents: project snapshot,
  architecture areas, non-negotiable technical rules, setup/test/lint/build
  commands, files to read first, risks/invariants, and high-value wiki links.
- `activity.md` - append-only activity log: when, which agent, trigger, intent,
  actions, files changed, validation, decisions, follow-up.
- `handoff.md` - pass-the-baton page: current work state, last completed step,
  prioritized next tasks, start files, done criteria, verification commands,
  blockers, risks, commands already run, work not to redo, and git state when
  available.

Use the reference templates when creating or repairing these pages:

- `references/agent-context-template.md`
- `references/agent-handoff-template.md`
- `references/work-tracker-template.md`

`agent/handoff.md` must include a `## Baton For Next Coding Agent` section with
this table:

```markdown
| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
```

Every next task must be verifiable. If verification is not currently possible,
write `Not verified - <reason>` instead of inventing a command.

At the end of a non-trivial task, update `<wiki-root>/agent/activity.md` and
`<wiki-root>/agent/handoff.md` if the wiki exists and the user has not opted out.
Also update `<wiki-root>/agent/context.md` and `<wiki-root>/project/work-tracker.md` when
project state, architecture, commands, risks, invariants, plans, blockers, or
next tasks change.

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
approval, then create a small but useful wiki. Engineering pages come first.

### Ingest

Deep-dive into a file, directory, feature, or topic. Update the module page and
any affected engineering, project, project-docs, agent, index, and log pages.

### Sync

Small, surgical update after source changes. Update only affected existing wiki
pages. If the change needs new pages or broad reorganization, recommend ingest.

### Lint

Read-only health report. Check staleness, drift, orphans, gaps,
contradictions, unsupported project-docs claims, project/engineering mismatch,
frontmatter, and legacy docs. Do not modify the wiki during lint unless the
user explicitly asks to save a report.

## Non-negotiable rules

1. Do not invent. If you cannot verify a claim, omit it or mark it as a gap.
2. Cite concrete evidence in `sources:`.
3. Engineering truth outranks project and communication pages.
4. Keep pages short enough to be useful. Split pages that grow past roughly 200
   lines.
5. Never modify source files during wiki operations.
6. Propose deletion or retirement; do not silently delete pages or legacy docs.
7. Update `index.md` whenever pages are added, renamed, or removed.
8. Update `log.md` after init, ingest, and sync. Lint is read-only by default.
9. Respect `<wiki-root>/SCHEMA.md` over these defaults.
10. Keep `overview-<project-slug>.md` current when project status, scope,
    milestones, important decisions, portfolio relevance, work relevance,
    research relevance, demos, publications, or reusable project material
    change.
11. Keep agent context and handoff evidence-based. Use `unknown`, `pending`, or
    `Not verified.` when source evidence is missing.
12. Each handoff task must include start files, done criteria, and a
    verification command or an explicit `Not verified - <reason>`.
