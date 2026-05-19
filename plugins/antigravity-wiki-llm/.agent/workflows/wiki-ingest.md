# /wiki-ingest [path-or-topic]

Deep-dive into a file, directory, or topic and update the repository-local
wiki.

## Preconditions

- If `wiki/` does not exist, tell the user to run `/wiki-init` first.
- If no target was provided, ask what to ingest.

## Resolve

- If the argument is an existing path, use it.
- If it is a topic, search the repository for relevant files and ask only when
  ambiguous.
- Announce the resolved target before editing.

## Read evidence

Read relevant source files, nearby dependencies, and related tests. For large
directories, sample public interfaces and major entry points.

## Update

For each affected page:

1. Read the current page first.
2. Make the smallest factual edit.
3. Update frontmatter.
4. Add supersession notes when correcting a previous claim.
5. Create a new page only when the target is a new coherent area.

Likely affected pages include `overview.md`, `modules/<area>.md`,
`architecture/decisions.md`, `architecture/data-model.md`, `glossary.md`,
`index.md`, and `log.md`.

## Log

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | <short description>
- Target: <path or topic>
- Pages created: <list or none>
- Pages updated: <list>
- Notable changes: <short facts>
- Follow-up: <item or none>
```

Never modify source files during ingest.
