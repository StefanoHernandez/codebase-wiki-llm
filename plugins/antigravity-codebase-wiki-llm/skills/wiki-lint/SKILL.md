---
name: wiki-lint
description: Run a read-only health check for staleness, drift, gaps, and unsupported claims. Use when the user says /wiki-lint, wiki lint, audit wiki, or check wiki health.
---

<!-- Generated from codebase/workflows/wiki-lint.md. Do not edit directly. -->

# /wiki-lint

Read-only health check for the repository-local wiki.

Requires the wiki maintainer skill. Respect `wiki/SCHEMA.md`.

## Step 1 - Preconditions

- If `wiki/` does not exist, tell the user to run `/wiki-init` first.
- Prefer git over mtimes when available.

## Step 2 - Gather facts

Read:

1. every wiki page frontmatter;
2. `wiki/SCHEMA.md`;
3. `wiki/index.md`;
4. current in-scope source/config/project files;
5. git status and recent commits;
6. root-level legacy docs listed by the schema.

Do targeted source reads only where needed to verify claims.

## Step 3 - Checks

### Staleness

Flag pages when:

- `updated` is older than schema policy and sources changed;
- five or more commits touched listed sources since `source_commit`;
- confidence is `low`;
- listed sources are missing.

### Drift

Flag claims contradicted by code, tests, configs, CI, or current project docs.

### Orphans

Flag pages not linked from `index.md` or another useful page. Ignore
`index.md`, `SCHEMA.md`, and append-only logs.

### Gaps

Flag important source areas, public interfaces, tests, config, operations,
project state, or agent handoff context that should be documented but is not.

### Engineering quality

Flag module pages missing important sections such as invariants, safe-change
guidance, verification, related tests, or failure modes when evidence exists.

### Project consistency

Flag roadmap/status/risk/requirement claims that are unsupported by project or
engineering evidence.

### Project-docs support

Flag communication claims that lack links to engineering, project, or source
evidence.

### Portable overview

Flag missing `wiki/overview-<project-slug>.md`.

Flag portable overview pages that:

- do not use lowercase kebab-case in the filename;
- lack `## Personal Wiki Export`;
- lack current status, technical areas, next steps, important decisions, or
  links to relevant technical wiki pages when evidence exists;
- contain personal motivation, career meaning, subjective importance, or user
  priorities that are not sourced or marked `Da confermare.`;
- contradict `overview.md`, `project/status.md`, `project/decisions.md`,
  engineering pages, or source evidence.

### Agent continuity

Flag missing or stale `wiki/agent/context.md`, `wiki/agent/activity.md`, or
`wiki/agent/handoff.md` when the schema expects them and recent non-trivial work
is visible.

### Contradictions

Flag disagreements across overview, engineering, modules, project,
project-docs, and source evidence.

### Legacy docs

For root-level legacy docs, propose retirement only when content is absorbed.
Never delete.

### Frontmatter hygiene

Flag missing fields, invalid dates, invalid confidence, and missing source
files.

## Step 4 - Report

Produce a concise markdown report:

```markdown
# Wiki Lint Report - YYYY-MM-DD

## Summary
<N> issues across <M> pages.
- Stale: <n>
- Drift: <n>
- Orphans: <n>
- Gaps: <n>
- Engineering quality: <n>
- Project consistency: <n>
- Project-docs support: <n>
- Portable overview: <n>
- Agent continuity: <n>
- Contradictions: <n>
- Legacy: <n>
- Frontmatter: <n>

## Findings
...

## Suggested follow-ups
...
```

## Step 5 - Read-only by default

Do not edit the wiki during lint. If the user explicitly asks to save the
report, write it under `wiki/lint-reports/` and append to `wiki/log.md`.

## Guardrails

- Do not modify source files.
- Do not delete or move legacy docs.
- If there are zero issues, say so plainly.
