---
title: SecondBrain context
activation: always-on
---

<!-- Generated from secondbrain/rules/secondbrain-context.md. Do not edit directly. -->

# SecondBrain context

Use the current directory as a SecondBrain vault when `SCHEMA.md`, `index.md`,
or a recognized vault structure exists.

## At the start of work

If `index.md` exists, read it early. It is the catalog of the vault.

If `SCHEMA.md` exists, read it before changing vault content. It defines active
domains, sensitivity rules, and page conventions for this vault.

If `inbox/` or `raw/` exists and the task concerns classification, research,
documents, meetings, projects, tasks, or expenses, inspect only the relevant
paths needed for the request.

## Boundaries

Operate only inside the current vault unless the user explicitly asks to read or
write elsewhere.

Preserve raw source material under `raw/`. Do not delete, rewrite, or move raw
files unless the user explicitly asks.

Do not invent personal meaning, motivation, priorities, career relevance, or
emotional significance. Use `Da confermare.` when unknown.

Use minimum necessary detail for sensitive documents, people, expenses, meeting
notes, client material, and personal administration.

## After completing non-trivial work

If vault content changed:

1. Append `log.md` with what changed, sources used, and follow-ups.
2. Update `index.md` when pages or domains were added, renamed, archived, or
   materially changed.
3. Keep links relative and source-backed.

Do not run `/secondbrain-sync` automatically if the user is still actively
deciding the vault structure.
