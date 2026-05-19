---
name: codebase-wiki-maintainer
description: Knowledge for maintaining a living LLM wiki for a codebase in Codex. Use whenever working with files under wiki/ or when running /wiki-init, /wiki-ingest, /wiki-sync, or /wiki-lint.
---

# Codebase Wiki Maintainer

This skill defines how Codex maintains a living wiki for a codebase.

The plugin is global. The wiki is not global. Every project keeps its own
`<repo>/wiki/` directory, with its own schema, pages, and log.

## Layers

1. Raw sources: source code and project documents outside `wiki/`. Read them as evidence.
2. Wiki: `<repo>/wiki/`. Codex owns this documentation layer during wiki operations.
3. Schema: `<repo>/wiki/SCHEMA.md`. Repo-specific conventions override this skill.

## Default wiki layout

```text
wiki/
├── SCHEMA.md
├── index.md
├── log.md
├── overview.md
├── architecture/
│   ├── decisions.md
│   └── data-model.md
├── modules/
└── glossary.md
```

## Page conventions

Every wiki page must have YAML frontmatter:

```yaml
---
title: Short descriptive title
updated: 2026-05-19
sources:
  - src/example.py
source_commit: abc123
confidence: high
---
```

Use standard Markdown links, tables, and Mermaid diagrams. Do not use
`[[wikilink]]` syntax.

## Confidence model

- `high`: written directly from current sources and no relevant source changes are known.
- `medium`: a few relevant changes occurred, or some claims are inferred.
- `low`: many relevant changes occurred, sources moved, or claims need review.

When code contradicts an old wiki claim, add a dated supersession note instead
of silently hiding the fact that the understanding changed.

## Wiki operations

- `/wiki-init`: bootstrap `wiki/` for the current repository.
- `/wiki-ingest [path]`: deliberate update from a file, directory, or topic.
- `/wiki-sync`: small post-task update from recent source changes.
- `/wiki-lint`: read-only audit for staleness, drift, orphans, gaps, contradictions, redundant legacy docs, and frontmatter issues.

## Non-negotiable rules

1. Do not invent claims. If a claim cannot be verified from source or docs, omit it or mark confidence low.
2. Cite source files in page frontmatter.
3. Read `wiki/SCHEMA.md` before editing wiki content when it exists.
4. Update `wiki/index.md` when pages are added, removed, renamed, or retitled.
5. Append `wiki/log.md` at the end of every wiki operation.
6. Never modify source files as part of a wiki operation.
7. Propose deletions, never execute them silently.
8. Keep pages focused; split pages that grow beyond roughly 200 lines.
