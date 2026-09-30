# Wiki context + auto-sync

Use the repository-local wiki at `<wiki-root>/` as durable project context whenever it
exists.

## Wiki root

{{include:partials/resolve-wiki-root.md}}

## At the start of work

Read `<wiki-root>/SCHEMA.md` `## Core map` first and use it to find every page
below by role. If SCHEMA has no `## Core map`, use the maintainer skill's v1 paths.

1. `index`: the catalog. Prefer wiki pages over re-reading source when they cover
   the topic; verify source when accuracy matters or confidence is low.
2. `context`: read when entering a repo or when the task depends on architecture,
   commands, invariants or risks. Its `Verified Facts` are not re-derived.
3. `handoff`: read before continuing unfinished work. If the session context says
   the handoff is N commits old, read it and say which handoff items no longer match the repo, and refresh it,
   before continuing.
4. `tracker`: read when the task depends on status, active or planned work,
   blockers or follow-up order.

If the wiki cannot answer, read source or project documents. If that reveals
durable knowledge, mention the gap or run `/wiki-ingest` when asked.

## After completing a non-trivial task

If source/config/project files changed and `<wiki-root>/` exists:

1. Run `/wiki-sync` unless the user opted out. It writes the `log` entry and
   updates `tracker` and `handoff`.
2. If you did not run it, append the `log` entry (SCHEMA `## Log format`) and
   update `tracker`/`handoff` yourself when the task changed project state, the
   plan, decisions or blockers, ran significant verification, or left work
   incomplete.
3. Update `context` when architecture, commands, invariants, risks or read-first
   files changed.
4. Every claim you write follows SCHEMA `## Evidence`: command, essential output,
   date, or `> ⚠️ NOT VERIFIED`.

Do not run `/wiki-sync` when no source/config/project files changed, the task is
still in progress across turns, or the user said not to update the wiki.

## Boundaries

- Do not modify files outside `<wiki-root>/` unless the user explicitly asks for a
  non-wiki project change; source files are read-only evidence.
- Never write a term listed in `<wiki-root>/.private-terms` outside that file.
- Host-specific packaging files are not part of a target project's wiki content.
