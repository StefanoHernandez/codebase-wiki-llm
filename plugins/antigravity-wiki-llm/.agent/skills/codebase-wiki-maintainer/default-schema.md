---
title: Wiki Schema
updated: 2026-05-19
confidence: high
---

# Wiki schema for this repo

This file is the repo-specific constitution for the wiki. Antigravity reads it
before wiki operations and follows these rules over pack defaults.

## Scope

In scope:
- Stable foundational code and architecture.
- Public APIs, service boundaries, core data models, and configuration.
- Architecture-shaping documents such as README files and design docs.

Out of scope:
- Fast-moving internal implementation details.
- Build artifacts, dependency folders, generated outputs, logs, caches, and
  binaries.
- `.git/`, `wiki/` itself, and tool cache directories.
- Lock files unless dependency analysis is explicitly requested.

## Directory layout

```text
wiki/
├── SCHEMA.md
├── index.md
├── log.md
├── overview.md
├── architecture/
│   ├── decisions.md
│   └── data-model.md
├── modules/
└── glossary.md
```

## Page granularity

- One module page per coherent area.
- One ADR entry per significant design decision.
- Glossary entries for project-specific terms that are not obvious to a new
  contributor.

## Decay policy

- Fast decay: `modules/*`, `architecture/data-model.md`, `overview.md`.
- Slow decay: `architecture/decisions.md`, `glossary.md`.
- Lower confidence when source files listed in frontmatter have changed and the
  page has not been re-verified.

## Redundant legacy docs

Lint may propose retirement for root-level docs once their content is absorbed:
- `context_map.md`
- `project_status.md`
- `BUILD_PHASES.md`
- `ARCHITECTURE.md`

Never delete automatically.

## Style preferences

- Use Mermaid for relationships, flows, and state machines.
- Use tables for APIs, config options, and schema mappings.
- Use standard relative Markdown links.
- Use ISO dates.
- Prefer concise, factual pages over broad narrative.

## Question policy

- `/wiki-init`: ask once to confirm the proposed scope before writing.
- `/wiki-ingest` with no target: ask what to ingest.
- `/wiki-sync`: do not ask; apply only small, clear updates.
- `/wiki-lint`: do not ask; produce a read-only report.
