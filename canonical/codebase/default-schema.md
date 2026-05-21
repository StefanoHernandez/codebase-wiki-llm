---
title: Wiki Schema
updated: 2026-05-19
confidence: high
---

# Wiki Schema for This Repo

This file is the repo-specific constitution for the wiki. Edit it when the
repository needs different conventions. Wiki workflows must read this file
before editing wiki content.

## Mission

This wiki is an engineering-first software project wiki. It exists to help
engineers change the software safely, help project leads understand state and
risk, preserve agent activity and handoff context, and prepare reusable project
documentation.

## Truth hierarchy

1. Source code, tests, migrations, configs, CI, and runtime manifests.
2. `wiki/engineering/` and `wiki/modules/`.
3. `wiki/project/`.
4. `wiki/project-docs/`.
5. `wiki/agent/` and historical logs.

Engineering is authoritative. Project and project-docs pages must not
contradict engineering pages or source evidence.

## Scope

**In scope**:

- Core architecture, module boundaries, data/control flows, and invariants.
- Public interfaces: APIs, CLIs, SDKs, jobs, events, services, and exported
  functions/classes.
- Development workflow: setup, commands, tests, linters, build, CI.
- Runtime/operations: configuration, env vars, deploy, migrations, external
  services, monitoring, troubleshooting.
- Project management: status, roadmap, milestones, requirements, risks, and
  decisions.
- Reusable project documentation: briefs, value proposition, use cases,
  audience, impact, evidence, demo material, FAQ.
- Agent continuity: context, activity, and handoff notes under `wiki/agent/`.

**Out of scope**:

- Generated artifacts, build output, caches, logs, fixtures, and vendored
  dependencies unless they define public behavior.
- Internal implementation details that change frequently and do not affect how
  engineers safely change the system.
- `.git/`, dependency folders, virtual environments, `dist/`, `build/`,
  `.next/`, `node_modules/`, `__pycache__/`, and lockfiles unless the repo
  schema explicitly says otherwise.
- Unsupported claims in `project-docs/`.

## Directory layout

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

## Page granularity

- One module page per coherent code area.
- Keep `engineering/` pages cross-cutting and operational.
- Keep `project/` pages about delivery state, requirements, risks, and
  decisions.
- Keep `project-docs/` pages reusable and evidence-backed.
- Keep `agent/` pages concise and useful for future sessions.
- Keep `overview-<project-slug>.md` as the portable project card for
  SecondBrain import.

## Portable project overview

Each project wiki must include:

```text
wiki/overview-<project-slug>.md
```

Use lowercase kebab-case for `<project-slug>`. This page is a concise,
portable summary of the project. It must link back to the detailed technical
wiki and include a `## Personal Wiki Export` section.

Required content:

- what the project is;
- why it exists;
- current status;
- main stack or technical areas;
- milestones or next steps;
- important decisions to remember;
- links to the most relevant engineering, module, project, and project-docs
  pages;
- `## Personal Wiki Export` for import into a general SecondBrain vault.

The `Personal Wiki Export` section should include:

- project name and short description;
- current status;
- role of the project in the user's work/life;
- personal motivation, only if known;
- technologies or skills represented;
- important next steps;
- long-term notes.

Do not invent personal motivation, career goals, subjective meaning, or user
priorities. If unknown, write `Da confermare.`

## Module page template

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

- Fast decay: `modules/*`, `engineering/data-model.md`,
  `engineering/testing.md`, `engineering/operations.md`,
  `engineering/change-map.md`.
- Medium decay: `overview.md`, `engineering/architecture.md`,
  `overview-<project-slug>.md`, `project/status.md`, `project/roadmap.md`,
  `project/risks.md`.
- Slow decay: `project/decisions.md`, `project-docs/*`, `glossary.md`,
  `agent/context.md`.

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
- `CHANGELOG.md` if it duplicates `wiki/agent/activity.md` or `wiki/log.md`

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
- `/wiki-sync`: do not ask; run only for small source changes.
- `/wiki-lint`: do not ask; produce a read-only report.

## What this repo is about

Replace this section during `/wiki-init` with one concise paragraph describing
the repository.
