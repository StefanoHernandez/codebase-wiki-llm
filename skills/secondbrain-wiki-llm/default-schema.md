---
title: SecondBrain Vault Schema
updated: 2026-05-21
confidence: high
---

<!-- Generated from secondbrain/default-schema.md. Do not edit directly. -->

# SecondBrain Vault Schema

This file is the vault-specific constitution for a personal and work knowledge
system. Agents must read it before editing vault content.

## Mission

The vault organizes the user's work and life material into a durable Markdown
knowledge system. It tracks projects, documents, meetings, research, tasks,
expenses, skills, people, publications, and long-term context while preserving
raw sources and protecting sensitive information.

## Truth hierarchy

1. Raw source material under `raw/`, user-provided files, links, transcripts,
   documents, statements, and explicitly supplied metadata.
2. Structured pages with current `sources:`.
3. `log.md` and historical entries.
4. Agent interpretation.

Raw material is evidence. Structured notes are maintained summaries and links.
Unknown personal context must be marked `Da confermare.`

## Core layout

Create these files and folders in every vault:

```text
index.md
SCHEMA.md
log.md
raw/
inbox/
archive/
```

## Optional domains

Activate only the domains the user wants to track or the source material
requires:

```text
projects/
work/
personal/
meetings/
research/
studies/
tasks/
expenses/
areas/
skills/
people/
publications/
```

Record active domains in this schema after initialization.

## Active domains

Replace this section during `/secondbrain-init` with the domains selected for
this vault and a one-line reason for each.

## Frontmatter

Structured pages should use:

```yaml
---
title: Short descriptive title
updated: 2026-05-21
type: project | document | meeting | research | task | expense | person | skill | area | publication | note
status: active | draft | waiting | archived | done | to-review
sensitivity: public | work | personal | sensitive
sources:
  - raw/example.md
confidence: high | medium | low
---
```

Use `sensitivity: sensitive` for identity, finance, health, legal, private
client, private meeting, or other highly personal material.

## Domain rules

- `raw/` is append-friendly source material. Do not rewrite or delete raw files
  unless the user explicitly asks.
- `inbox/` is temporary. Prefer classification into structured domains.
- `projects/` pages must include status, purpose, related documents, related
  meetings, related tasks, related research, and next steps when known.
- `meetings/` pages must distinguish decisions from action items and mark
  unknown owners or due dates as `Da confermare.`
- `research/` pages must distinguish sources, synthesis, interpretation, ideas,
  and next steps.
- `tasks/` pages or task registers must include status and source when derived
  from a meeting, document, or project.
- `expenses/` entries must avoid lifestyle inference. Record category,
  date, amount, source, and recurrence only when evidence supports them.
- `people/` pages must use minimum necessary personal detail.

## Style preferences

- Use relative Markdown links.
- Use tables for tasks, expenses, project status, document registers, source
  support, and meeting action items.
- Keep pages short enough to be useful. Split large pages when needed.
- Prefer explicit "No verified content yet" notes over generic filler.

## Question policy

- `/secondbrain-init`: ask once to confirm the proposed adaptive structure
  before writing.
- `/secondbrain-ingest` without a target: ask what to ingest.
- `/secondbrain-sync`: do not ask for small updates; report when ingest is more
  appropriate.
- `/secondbrain-lint`: do not ask; produce a read-only report.
