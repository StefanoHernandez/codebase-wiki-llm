# /wiki-sync

Fast incremental update of existing wiki pages after small source changes.

## Preconditions

- If `wiki/` does not exist, exit quietly.
- If no relevant source files changed, report `wiki-sync: nothing to do.`

## Determine changes

Prefer git:

- `git status --porcelain`
- `git diff --name-only HEAD`
- For existing wiki pages, compare `source_commit` against current `HEAD` for
  listed sources.

Filter out `wiki/`, build outputs, dependency folders, caches, binaries, and
anything excluded by `wiki/SCHEMA.md`.

## Map pages

Update pages whose `sources:` frontmatter includes changed files. Also consider
module pages that mention the changed module.

If more than roughly 10 pages are affected, do not auto-sync. Report that the
change is too large and recommend `/wiki-ingest` or `/wiki-lint`.

## Apply

For each affected page:

1. Re-read the page and changed sources.
2. Apply minimum factual edits.
3. Update frontmatter.
4. Add supersession notes where an old claim changed.

Do not create new pages during sync. Recommend `/wiki-ingest` when a new page is
needed.

## Log

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] sync | <N> pages updated
- Changed files: <short list or count>
- Pages updated: <list>
- Follow-ups: <item or none>
```
