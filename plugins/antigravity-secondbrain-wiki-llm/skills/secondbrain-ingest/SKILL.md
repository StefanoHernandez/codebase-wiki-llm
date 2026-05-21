---
name: secondbrain-ingest
description: Ingest raw material, inbox notes, files, folders, links, or topics into the vault. Use when the user says /secondbrain-ingest, secondbrain ingest, ingest raw material, classify inbox, or add files/links/notes to a vault.
---

<!-- Generated from secondbrain/workflows/secondbrain-ingest.md. Do not edit directly. -->

# /secondbrain-ingest

Ingest raw material, inbox notes, files, folders, links, or topics into the
SecondBrain vault.

Requires the SecondBrain maintainer skill. Respect `SCHEMA.md`.

## Step 1 - Preconditions

- If `SCHEMA.md` or `index.md` is missing, recommend `/secondbrain-init`.
- If no target is provided, ask what to ingest.
- If the target is outside the vault, ask before reading it.

## Step 2 - Inspect target

Read only the material needed for the requested ingest.

Classify the target as one or more domains:

- project overview or project material;
- work document, proposal, deliverable, report, or client material;
- personal document, certification, administration, or finance material;
- meeting note or transcript;
- research material, paper, video, link list, report, or topic;
- study material;
- task or follow-up;
- expense or receipt;
- person/contact/stakeholder note;
- publication or public-facing draft;
- unknown inbox material.

## Step 3 - Preserve evidence

Keep raw source material intact. If the material is not already under `raw/` or
`inbox/`, link to it as a source or ask before copying it into the vault.

Every structured page derived from the target must include `sources:`.

## Step 4 - Create or update structured notes

Apply the appropriate domain template:

- Project: status, purpose, role, linked documents, meetings, tasks, research,
  skills, next steps.
- Work document: document type, context, project/client, summary, decisions,
  obligations, follow-ups, source.
- Personal document: document type, purpose, date if known, sensitivity,
  renewal or follow-up if known, source.
- Meeting: summary, context, participants, decisions, action items, blockers,
  follow-ups, linked project/person/document, source.
- Research: research question, sources, synthesis, concepts, interpretation,
  related projects, related skills, publication ideas, next steps.
- Study: learning objective, resources, progress, exercises, gaps, next session.
- Task: description, status, source, owner if known, due date if known, linked
  project/document/meeting.
- Expense: date, category, amount if known, source, recurrence if verified,
  status.
- Person: relevance, relationship, linked projects/meetings/documents, minimum
  necessary personal detail.
- Publication: target audience, outline, claims, source support, status.

Use `Da confermare.` for unknown personal meaning, motivations, priorities,
owners, due dates, or subjective importance.

## Step 5 - Link and update indexes

Update relevant index pages and `index.md` when new pages are created.

Link related notes across domains when evidence supports the relationship.

## Step 6 - Append log

Append to `log.md`:

```markdown
## [YYYY-MM-DD] ingest | <target>
- Domains: <list>
- Sources: <short list>
- Pages created: <list or none>
- Pages updated: <list or none>
- Follow-ups: <none or list>
```

## Step 7 - Report

Report:

- what was ingested;
- pages created or updated;
- sensitive items handled cautiously;
- facts marked `Da confermare.`;
- recommended next step.

## Guardrails

- Do not delete raw material.
- Do not over-classify uncertain material.
- Do not duplicate sensitive values unnecessarily.
- If ingestion would create many pages, propose a staged plan first.
