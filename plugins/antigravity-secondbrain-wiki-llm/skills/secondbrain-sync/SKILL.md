---
name: secondbrain-sync
description: Surgically update an existing SecondBrain vault after small changes. Use when the user says /secondbrain-sync, secondbrain sync, update vault from recent changes, or asks to refresh existing vault notes.
---

<!-- Generated from secondbrain/workflows/secondbrain-sync.md. Do not edit directly. -->

# /secondbrain-sync

Fast, surgical update for an existing SecondBrain vault.

Requires the SecondBrain maintainer skill. Respect `SCHEMA.md`.

## Step 1 - Fast preconditions

- If `SCHEMA.md` or `index.md` does not exist, exit and recommend
  `/secondbrain-init`.
- If there are no relevant changes in `raw/`, `inbox/`, or structured pages,
  report `secondbrain-sync: nothing to do.`

## Step 2 - Determine changes

Prefer git when available:

1. `git status --porcelain` for uncommitted and untracked files.
2. `git diff --name-only HEAD` for working-tree changes.
3. For structured pages, compare `sources:` against changed raw/source files.

If git is unavailable, use mtimes and recent file changes.

Ignore caches, generated previews, app metadata, and archive material unless the
user explicitly asks.

## Step 3 - Map changes to pages

Map common changes:

- raw project material -> `projects/*`;
- work documents -> `work/*`, `projects/*`, `tasks/*`;
- personal documents -> `personal/*`, `tasks/*`;
- meetings -> `meetings/*`, `tasks/*`, `projects/*`, `people/*`;
- research material -> `research/*`, `skills/*`, `projects/*`,
  `publications/*`;
- expenses -> `expenses/*`;
- inbox items -> domain pages or a triage report;
- schema/index changes -> `index.md` and relevant domain index pages.

If more than roughly 10 pages are affected, stop and recommend
`/secondbrain-ingest` or staged sync.

## Step 4 - Update affected existing pages

Apply minimum edits:

- update status, summaries, source links, task state, action items, and
  follow-ups;
- add new evidence-backed relationships;
- update frontmatter `updated`, `sources`, `status`, `confidence`, and
  `sensitivity` when needed;
- mark uncertain personal facts as `Da confermare.`;
- avoid broad rewrites.

Do not create many new pages during sync. If new domains or many pages are
needed, recommend ingest.

## Step 5 - Update indexes and log

Touch `index.md` and domain indexes only when page availability, summaries, or
domain status changed.

Append to `log.md`:

```markdown
## [YYYY-MM-DD] sync | <N> pages updated
- Changed inputs: <short list or count>
- Pages updated: <list>
- Follow-ups: <none or list>
```

## Step 6 - Report

Keep output short:

- `secondbrain-sync: nothing to do.`
- or `secondbrain-sync: updated <pages> based on <inputs>. <follow-up>`

## Guardrails

- Do not delete raw material.
- Do not infer sensitive or personal meaning.
- Do not write outside the vault.
- If unsure whether the change is small, recommend ingest.
