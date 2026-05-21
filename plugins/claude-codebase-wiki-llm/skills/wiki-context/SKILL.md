---
name: wiki-context
description: Use a repository-local wiki as project context and keep agent continuity current.
---

<!-- Generated from codebase/rules/wiki-context.md. Do not edit directly. -->

# Wiki context + auto-sync

Use the repository-local wiki at `wiki/` as durable project context whenever it
exists.

## At the start of work

If `wiki/index.md` exists, read it early. It is the catalog of project
knowledge. Prefer wiki pages over re-reading source code when the wiki already
covers the topic, but verify source files when accuracy matters or the wiki is
low confidence.

If `wiki/agent/context.md` or `wiki/agent/handoff.md` exists, read it when the
task depends on prior agent work, current project state, or unfinished work.

## When the wiki cannot answer

Read source code or project documents as needed. If the answer reveals durable
knowledge that belongs in the wiki, mention the gap or run `/wiki-ingest` when
the user asks you to update the wiki.

## After completing a non-trivial task

If source/config/project files changed and `wiki/` exists:

1. Run `/wiki-sync` unless the user opted out.
2. Update `wiki/agent/activity.md` and `wiki/agent/handoff.md` when the task
   changed project state, made decisions, or created useful handoff context.

Do not run `/wiki-sync` when:

- no source/config/project files changed;
- the user task is still in progress across turns;
- the user explicitly said not to update the wiki.

## Boundaries

Wiki workflows may read source files as evidence, but they must not modify files
outside `wiki/` unless the user explicitly asks for a non-wiki project change.
Host-specific packaging files are source files for this plugin repository and
are not part of a target project's wiki content.
