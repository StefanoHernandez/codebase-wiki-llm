# /wiki-lint

Audit the repository-local wiki for health. Produce a report; do not fix issues
automatically.

## Preconditions

- If `wiki/` does not exist, tell the user to run `/wiki-init` first.
- If `wiki/SCHEMA.md` exists, read it before checking pages.
- Prefer git history over filesystem mtimes when available.

## Checks

1. Staleness: pages whose sources changed since `source_commit`, old `updated`
   dates, or low confidence.
2. Drift: specific claims that contradict current code.
3. Orphans: wiki pages not linked from `index.md` or other pages.
4. Gaps: important source areas with no wiki coverage.
5. Contradictions: pages that disagree with each other.
6. Redundant legacy docs: root docs whose content is already absorbed.
7. Frontmatter hygiene: missing fields, invalid dates, missing sources.

## Report

Use this format:

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

Never delete, move, or edit source files during lint.
