# Codebase Wiki LLM for Antigravity

This pack maintains a living, repository-local wiki under `<repo>/wiki/`.

Use it for:

- `/wiki-init`: bootstrap a new `wiki/`.
- `/wiki-ingest [path-or-topic]`: document a specific area.
- `/wiki-sync`: update existing wiki pages after small source changes.
- `/wiki-lint`: audit wiki health and report drift, gaps, stale pages, and
  frontmatter issues.

Guardrails:

- Never invent wiki claims. Verify from source files or mark uncertainty.
- Cite source files in page frontmatter.
- Read `wiki/SCHEMA.md` before editing wiki pages when it exists.
- Never modify source files during wiki operations.
- Propose deletions; do not silently delete pages or legacy docs.
