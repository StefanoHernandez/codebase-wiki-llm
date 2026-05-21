# Wiki Maintainer

This skill maintains an engineering-first software project wiki under
`<repo>/wiki/`. The wiki is durable project knowledge for software engineers,
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

## Truth hierarchy

When sources disagree, use this order:

1. Source code, tests, migrations, configs, CI, and runtime manifests.
2. `wiki/engineering/` and `wiki/modules/`.
3. `wiki/project/`.
4. `wiki/project-docs/`.
5. `wiki/agent/` and historical logs.

`engineering/` and `modules/` are authoritative for technical reality.
`project/` summarizes delivery state and decisions. `project-docs/` reuses and
communicates supported claims; it must not invent capabilities.

## The three layers

1. **Raw sources** - code, tests, configs, docs, manifests, CI, issue exports,
   meeting notes, and proposal material. Read them as evidence. During wiki
   operations, do not modify files outside `wiki/`.
2. **The wiki** - `<repo>/wiki/`. The agent owns this knowledge layer and keeps
   it useful, accurate, and navigable.
3. **The schema** - `<repo>/wiki/SCHEMA.md`. Repo-specific conventions override
   these defaults. Read it before any wiki operation.

## Default wiki structure

```text
wiki/
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
wiki/overview-<project-slug>.md
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

`wiki/project/` describes project management state: roadmap, milestones, risks,
requirements, and decisions. It should link to technical evidence rather than
duplicating technical details.

Risk entries should include impact, evidence, mitigation, owner if known, and
status. Decisions should include context, decision, rationale, consequences, and
links to affected engineering pages.

## Project-docs layer

`wiki/project-docs/` stores reusable communication material for READMEs,
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

`wiki/agent/` replaces scattered project-context files. It records what agents
need to know and what they did.

- `context.md` - concise current context for future agents.
- `activity.md` - append-only activity log: when, which agent, trigger, intent,
  actions, files changed, validation, decisions, follow-up.
- `handoff.md` - current task, last completed step, next recommended step,
  blockers, files to inspect first, commands already run.

At the end of a non-trivial task, update `wiki/agent/activity.md` and
`wiki/agent/handoff.md` if the wiki exists and the user has not opted out.

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
9. Respect `wiki/SCHEMA.md` over these defaults.
10. Keep `overview-<project-slug>.md` current when project status, scope,
    milestones, important decisions, portfolio relevance, work relevance,
    research relevance, demos, publications, or reusable project material
    change.
