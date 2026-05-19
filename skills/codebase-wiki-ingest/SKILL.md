---
name: codebase-wiki-ingest
description: Deep-dive into a file, directory, or topic and update the repository-local wiki. Use when the user says /wiki-ingest, wiki ingest, document this area in the wiki, or asks to add source knowledge to wiki/.
---

# Codebase Wiki Ingest

Handle `/wiki-ingest [path-or-topic]` for the current repository.

Load `codebase-wiki-maintainer` first and respect `wiki/SCHEMA.md`.

## Preconditions

- If `wiki/` does not exist, tell the user to run `/wiki-init` first.
- If no target was provided, ask what to ingest.

## Resolve target

- If the argument is an existing path, use it.
- If it is a topic, search the repo for relevant files and ask only if ambiguous.
- Announce the resolved target before editing.

## Read evidence

Read relevant source files, nearby dependencies, and related tests. Keep the
scope deliberate. For large directories, sample by public interfaces and major
entry points.

## Update pages

Decide which pages are affected:
- `overview.md`
- `modules/<area>.md`
- `architecture/decisions.md`
- `architecture/data-model.md`
- `glossary.md`
- `index.md`
- `log.md`

For each page:
1. Read the current page first.
2. Make the smallest factual edit.
3. Update frontmatter.
4. Add supersession notes for corrected claims.
5. Create a new page only when the target is a new coherent area.

## Log format

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | <short description>
- Target: <path or topic>
- Pages created: <list or none>
- Pages updated: <list>
- Notable changes: <short facts>
- Follow-up: <item or none>
```

## Report

Summarize created pages, updated pages, and any follow-up. Never modify source
files during ingest.
