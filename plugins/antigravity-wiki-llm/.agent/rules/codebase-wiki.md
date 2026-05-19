# Codebase Wiki Rule

Apply these rules whenever work involves a repository-local `wiki/` directory
or a wiki command such as `/wiki-init`, `/wiki-ingest`, `/wiki-sync`, or
`/wiki-lint`.

## Scope

The wiki belongs to the current project. It lives under `<repo>/wiki/` and is
not a shared global wiki.

## Mandatory behavior

- If `wiki/index.md` exists and the user asks about architecture, modules,
  onboarding, roadmap, or project context, read it early.
- If `wiki/SCHEMA.md` exists, read it before editing wiki pages.
- Treat source code and project docs outside `wiki/` as evidence.
- During wiki operations, write only under `wiki/`.
- Never change source files as part of a wiki operation.
- Use standard Markdown links, frontmatter, concise factual prose, tables, and
  Mermaid diagrams where useful.
- Add or update `wiki/index.md` when wiki pages are created, renamed, removed,
  or retitled.
- Append `wiki/log.md` at the end of write operations.
- Propose deletions or retirement of legacy docs; do not execute them silently.

## Confidence

Use `confidence: high`, `medium`, or `low` in wiki frontmatter.

- `high`: verified directly against current sources.
- `medium`: mostly verified, but some claims are inferred or source changes are
  nearby.
- `low`: stale, ambiguous, or based on incomplete evidence.
