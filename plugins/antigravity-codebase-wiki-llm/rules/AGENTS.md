<!-- Generated from codebase/rules/wiki-context.md. Do not edit directly. -->

# Wiki context + auto-sync

Use the repository-local wiki at `<wiki-root>/` as durable project context whenever it
exists.

## Wiki root

In these instructions, `<wiki-root>` is this repository's wiki directory,
relative to the repository root (`wiki` by default). Resolve it once, before
anything else, use the resolved value in every wiki path, and state it:
`Wiki root: <value>/`.

1. If your context contains a line `Codebase Wiki LLM: wiki_root: <value>`
   (added when the session started) and you have not created or changed the
   wiki root during this session, use `<value>`.
2. Otherwise, if `.wikidir` exists at the repository root, read that file
   directly: its first non-empty line is the folder name. Do not look for it
   with a file search: searches skip hidden and gitignored files.
3. Otherwise, if `wiki/SCHEMA.md` exists, `<wiki-root>` is `wiki`.
4. Otherwise the repository has no wiki yet.

The value must be a single directory name matching
`^\.?[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9_-])?$` (no trailing dot) and must
not be one of `.git`, `.github`, `.claude`, `.codex`, `.agents`, `.agent`,
`.gemini`, `.opencode`, `.obsidian`, `.vscode`, `node_modules`, `.wikidir`,
compared case-insensitively. If it breaks these rules or names a directory
that does not exist, stop and tell the user without guessing another location.

## At the start of work

Read `<wiki-root>/SCHEMA.md` `## Core map` first and use it to find every page
below by role. If SCHEMA has no `## Core map`, use the v1 default paths.

1. `index`: the catalog. Prefer wiki pages over re-reading source when they cover
   the topic; verify source when accuracy matters or confidence is low.
2. `context`: read when entering a repo or when the task depends on architecture,
   commands, invariants or risks. Its `Verified Facts` are not re-derived.
3. `handoff`: read before continuing unfinished work. If the session context says
   the handoff is N commits old, read it and say what is stale before continuing.
4. `tracker`: read when the task depends on status, active or planned work,
   blockers or follow-up order.

If the wiki cannot answer, read source or project documents. If that reveals
durable knowledge, mention the gap or run `/wiki-ingest` when asked.

## After completing a non-trivial task

If source/config/project files changed and `<wiki-root>/` exists:

1. Run `/wiki-sync` unless the user opted out.
2. Append a `log` entry in SCHEMA `## Log format`.
3. Update `handoff` and `tracker` when the task changed project state, the plan,
   decisions or blockers, ran significant verification, or left work incomplete.
4. Update `context` when architecture, commands, invariants, risks or read-first
   files changed.
5. Every claim you write follows SCHEMA `## Evidence`: command, essential output,
   date, or `> ⚠️ NOT VERIFIED`.

Do not run `/wiki-sync` when no source/config/project files changed, the task is
still in progress across turns, or the user said not to update the wiki.

## Boundaries

- Do not modify files outside `<wiki-root>/` unless the user explicitly asks for a
  non-wiki project change; source files are read-only evidence.
- Never write a term listed in `.private-terms` outside that file.
- Host-specific packaging files are not part of a target project's wiki content.
