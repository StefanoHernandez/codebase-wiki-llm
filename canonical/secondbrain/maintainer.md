# SecondBrain Maintainer

This skill maintains a vault-local personal and work knowledge system. The
vault is a Markdown workspace for projects, work documents, personal documents,
meetings, research, tasks, expenses, skills, people, publications, and long-term
operational memory.

The primary reader is the user who needs a reliable overview of work and life
material without losing source traceability. Secondary readers are future
agents helping the user search, summarize, classify, plan, and produce reusable
material from the vault.

Optimize every page for fast answers to:

- what is this item?
- why is it in the vault?
- where did this claim come from?
- what project, document, meeting, task, research topic, or person is it linked
  to?
- what needs action, review, confirmation, or archival?

## Truth hierarchy

When sources disagree, use this order:

1. Raw source material under `raw/`, user-provided files, transcripts, links,
   documents, statements, and explicitly supplied metadata.
2. Structured vault pages whose `sources:` still point to current evidence.
3. `log.md` and historical entries.
4. Agent interpretation.

Raw material is evidence. Structured notes are the maintained knowledge layer.
Interpretation must be labeled and must never override concrete source
material.

## The three layers

1. **Raw inputs** - imported files, links, notes, project overview exports,
   meeting notes, transcripts, receipts, certificates, proposals, reports,
   papers, videos, and other source material. Keep raw content intact unless
   the user explicitly asks for cleanup.
2. **The vault** - the current directory. The agent organizes durable knowledge
   into structured Markdown pages and links related material.
3. **The schema** - `SCHEMA.md`. Vault-specific conventions override these
   defaults. Read it before any vault operation.

## Adaptive vault structure

Every vault should have a small core:

```text
index.md
SCHEMA.md
log.md
raw/
inbox/
archive/
```

Optional domains are activated during `/secondbrain-init` or later ingest:

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

Do not create a large empty taxonomy by default. Create a domain when the user
asks for it, when source material clearly needs it, or when it is necessary to
organize imported material safely.

## Domain guidance

- `projects/` - personal, work, research, and software project overview pages.
- `work/` - proposals, deliverables, client material, reports, meetings, and
  work documents.
- `personal/` - personal documents, certifications, administration, and finance
  material.
- `meetings/` - structured meeting notes with decisions, action items, blockers,
  follow-ups, participants, linked projects, and source material.
- `research/` - source-backed topic notes with questions, synthesis, concepts,
  sources, related projects, related skills, and next steps.
- `studies/` - learning tracks, resources, progress, exercises, gaps, and next
  sessions.
- `tasks/` - operational work, follow-ups, due dates, status, owners if known,
  linked projects, and source references.
- `expenses/` - expense records, categories, dates, amount if known, source,
  recurrence only when verified, and status.
- `areas/` - long-running areas of life or work that group projects, research,
  tasks, documents, and goals.
- `skills/` - capabilities, evidence, projects demonstrating the skill, related
  studies, gaps, and next steps.
- `people/` - contacts, authors, clients, collaborators, stakeholders, and why
  they are relevant. Use minimum necessary personal detail.
- `publications/` - drafts, posts, talks, proposals, case studies, abstracts,
  claim support, and source links.

## Page conventions

Every structured vault page should have YAML frontmatter:

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

Rules:

- `sources:` must name concrete evidence files or links when the page is derived
  from material.
- `sensitivity:` is required for documents, people, personal, expenses, and
  meeting pages.
- Use standard relative Markdown links. Do not use `[[wikilink]]` syntax.
- Prefer tables for tasks, document registers, expenses, people maps, project
  status, and source support.
- Use `Da confermare.` for personal meaning, motivations, priorities, career
  implications, or sensitive details that are not explicitly known.

## Sensitive information

Treat personal documents, identity documents, certifications, financial data,
health material, expenses, contracts, client information, and private meeting
notes with minimum necessary detail.

Do not duplicate sensitive values across pages unless required for the task.
Prefer references such as "see source document" over copying full identifiers,
addresses, account numbers, private notes, or other sensitive content.

If the sensitivity is unclear, use `sensitivity: personal` or
`sensitivity: sensitive` and ask the user before broadening exposure.

## Ingest behavior

`/secondbrain-ingest` is domain-aware. It should classify the input and apply
the right template:

- raw project exports -> `projects/`;
- work documents -> `work/documents/`, `work/proposals/`, or
  `work/deliverables/`;
- personal documents -> `personal/documents/`, `personal/certifications/`, or
  `personal/admin/`;
- meeting notes or transcripts -> `meetings/` plus linked tasks/projects/people
  when useful;
- research material, papers, videos, links, and reports -> `research/` and
  related `skills/`, `projects/`, or `publications/`;
- expenses or receipts -> `expenses/`;
- unclassified notes -> `inbox/` triage or a structured note with
  `status: to-review`.

When a file does not clearly fit, keep it in `inbox/` and mark unknown facts as
`Da confermare.`

## Operations

### Init

Survey existing files and the user's stated goals. Propose an adaptive vault
structure, ask once for confirmation, then create only the core and selected
domains.

### Ingest

Deep-dive into a file, folder, link list, topic, or inbox item. Preserve raw
sources, create or update structured notes, link related pages, and record
follow-ups.

### Sync

Make small, surgical updates after raw inputs or structured notes changed.
Update affected existing pages, indexes, logs, and task/status links. If broad
reorganization is needed, recommend ingest.

### Lint

Read-only health report. Check unprocessed raw items, inbox backlog,
frontmatter, broken links, missing sources, unsupported personal claims,
sensitive-data handling, stale projects, meeting action items, task status,
research source quality, duplicate pages, and orphan notes.

## Non-negotiable rules

1. Do not invent personal meaning, motivation, priority, career value, or
   emotional significance. Use `Da confermare.` when unknown.
2. Do not write outside the current vault unless the user explicitly asks.
3. Preserve raw source material.
4. Cite concrete source material in `sources:`.
5. Protect sensitive information with minimum necessary detail.
6. Keep `inbox/` transitory and report items that need classification.
7. Keep `index.md` useful whenever pages or domains are added.
8. Append `log.md` after init, ingest, and sync. Lint is read-only by default.
9. Respect `SCHEMA.md` over these defaults.
