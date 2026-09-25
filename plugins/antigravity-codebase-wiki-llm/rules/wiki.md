---
title: Wiki context + auto-sync
activation: always-on
---

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

If `<wiki-root>/index.md` exists, read it early. It is the catalog of project
knowledge. Prefer wiki pages over re-reading source code when the wiki already
covers the topic, but verify source files when accuracy matters or the wiki is
low confidence.

If `<wiki-root>/agent/context.md` exists, read it when entering an existing repo or
when the task depends on architecture, setup, test commands, invariants, or
project risks.

If `<wiki-root>/agent/handoff.md` exists, read it before continuing unfinished work.
The `Baton For Next Coding Agent` section is the prioritized continuation
queue.

If `<wiki-root>/project/work-tracker.md` exists, read it when the task depends on
project status, active work, planned work, blockers, or follow-up order.

## When the wiki cannot answer

Read source code or project documents as needed. If the answer reveals durable
knowledge that belongs in the wiki, mention the gap or run `/wiki-ingest` when
the user asks you to update the wiki.

## After completing a non-trivial task

If source/config/project files changed and `<wiki-root>/` exists:

1. Run `/wiki-sync` unless the user opted out.
2. Update `<wiki-root>/agent/activity.md`, `<wiki-root>/agent/handoff.md`, and
   `<wiki-root>/project/work-tracker.md` when the task changed project state, changed
   the plan, made decisions, introduced blockers, ran significant verification,
   or left incomplete work.
3. Update `<wiki-root>/agent/context.md` when architecture, commands, invariants,
   risks, or read-first files changed.

Do not run `/wiki-sync` when:

- no source/config/project files changed;
- the user task is still in progress across turns;
- the user explicitly said not to update the wiki.

## Boundaries

Wiki workflows may read source files as evidence, but they must not modify files
outside `<wiki-root>/` unless the user explicitly asks for a non-wiki project change.
Host-specific packaging files are source files for this plugin repository and
are not part of a target project's wiki content.
