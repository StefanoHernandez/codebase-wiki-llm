---
name: secondbrain-lint
description: Run a read-only health check for a SecondBrain vault.
---

<!-- Generated from secondbrain/workflows/secondbrain-lint.md. Do not edit directly. -->

# /secondbrain-lint

Run a read-only health check for a SecondBrain vault.

Requires the SecondBrain maintainer skill. Respect `SCHEMA.md`.

## Scope

Inspect the vault structure, active domains, indexes, raw/inbox backlog,
frontmatter, source traceability, sensitivity handling, links, stale pages,
duplicates, and operational gaps.

Do not modify files unless the user explicitly asks to save a report.

## Checks

### Structure

- `index.md`, `SCHEMA.md`, `log.md`, `raw/`, `inbox/`, and `archive/` exist.
- Active domains listed in `SCHEMA.md` have matching folders.
- Domain folders have index pages when useful.
- `index.md` links to active domains and key pages.

### Frontmatter

Flag structured pages missing:

- `title`;
- `updated`;
- `type`;
- `status`;
- `sensitivity`;
- `sources` when derived from raw material;
- `confidence`.

### Source traceability

Flag:

- pages with claims but no source;
- missing files listed in `sources:`;
- raw files not referenced by any structured page;
- inbox items not classified or triaged.

### Sensitive data

Flag:

- personal, finance, identity, health, client, legal, or meeting material
  without appropriate `sensitivity`;
- duplicated sensitive values across pages;
- unnecessary sensitive detail copied from raw sources.

### Personal meaning

Flag subjective claims that are not sourced:

- personal motivation;
- career relevance;
- emotional significance;
- priority;
- life/work role;
- inferred habits.

These should be removed or marked `Da confermare.`

### Domain health

Check:

- projects without status or next step;
- meetings without decisions/action items review;
- tasks without status;
- research without sources or next steps;
- expenses without date/category/source where applicable;
- people without reason for relevance;
- publications without source-backed claims;
- orphan pages with no incoming or outgoing links.

### Drift and duplication

Flag:

- duplicate notes for the same entity;
- pages whose sources changed since they were last updated when git is
  available;
- stale `status: active` pages with no recent source support.

## Output format

Produce:

```markdown
# SecondBrain lint report

## Summary
- Health: pass | warnings | fail
- Critical issues: <count>
- Warnings: <count>
- Suggestions: <count>

## Critical issues
...

## Warnings
...

## Suggestions
...

## Suggested next commands
...
```

## Guardrails

- Read-only by default.
- Do not expose sensitive values in the report; refer to page paths and issue
  types instead.
- Prefer concrete file paths and fixes over generic advice.
