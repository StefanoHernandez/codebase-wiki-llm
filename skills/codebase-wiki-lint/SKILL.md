---
name: codebase-wiki-lint
description: Audit a repository-local wiki for staleness, drift, orphans, gaps, contradictions, redundant docs, and frontmatter issues. Use when the user says /wiki-lint, wiki lint, audit wiki, or check wiki health.
---

# Codebase Wiki Lint

Handle `/wiki-lint` for the current repository.

Load `codebase-wiki-maintainer` first and respect `wiki/SCHEMA.md`.

Lint is read-only. Do not edit files during lint except appending to `wiki/log.md`
if the lint operation is completed.

## Checks

1. Staleness: pages whose sources changed since `source_commit`, old `updated` dates, or low confidence.
2. Drift: specific claims that contradict current code.
3. Orphans: wiki pages not linked from `index.md` or other pages.
4. Gaps: important source areas with no wiki coverage.
5. Contradictions: pages that disagree with each other.
6. Redundant legacy docs: root docs whose content is already absorbed.
7. Frontmatter hygiene: missing fields, invalid dates, missing sources.

## Method

1. List wiki pages and read frontmatter.
2. Read `wiki/SCHEMA.md`.
3. Compare listed `sources:` with current files.
4. Use git history where available.
5. Spot-check code only where needed to validate drift or gaps.

## Report format

```markdown
# Wiki Lint Report - YYYY-MM-DD

## Summary
<N> issues found across <M> pages.

## Stale pages
- ...

## Drift
- ...

## Orphans
- ...

## Gaps
- ...

## Contradictions
- ...

## Redundant legacy docs
- ...

## Frontmatter hygiene
- ...

## Suggested follow-ups
1. ...
```

## Log

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] lint | <N> issues across <M> pages
- Stale: <n>, Drift: <n>, Orphans: <n>, Gaps: <n>, Contradictions: <n>, Legacy: <n>, Frontmatter: <n>
- Report: see chat
```

Never delete, move, or edit source files during lint.
