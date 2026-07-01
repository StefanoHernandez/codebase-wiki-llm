# Wiki context + auto-sync

Use the repository-local wiki at `wiki/` as durable project context whenever it
exists.

## At the start of work

If `wiki/index.md` exists, read it early. It is the catalog of project
knowledge. Prefer wiki pages over re-reading source code when the wiki already
covers the topic, but verify source files when accuracy matters or the wiki is
low confidence.

If `wiki/agent/context.md` exists, read it when entering an existing repo or
when the task depends on architecture, setup, test commands, invariants, or
project risks.

If `wiki/agent/handoff.md` exists, read it before continuing unfinished work.
The `Baton For Next Coding Agent` section is the prioritized continuation
queue.

If `wiki/project/work-tracker.md` exists, read it when the task depends on
project status, active work, planned work, blockers, or follow-up order.

## When the wiki cannot answer

Read source code or project documents as needed. If the answer reveals durable
knowledge that belongs in the wiki, mention the gap or run `/wiki-ingest` when
the user asks you to update the wiki.

## After completing a non-trivial task

If source/config/project files changed and `wiki/` exists:

1. Run `/wiki-sync` unless the user opted out.
2. Update `wiki/agent/activity.md`, `wiki/agent/handoff.md`, and
   `wiki/project/work-tracker.md` when the task changed project state, changed
   the plan, made decisions, introduced blockers, ran significant verification,
   or left incomplete work.
3. Update `wiki/agent/context.md` when architecture, commands, invariants,
   risks, or read-first files changed.

Do not run `/wiki-sync` when:

- no source/config/project files changed;
- the user task is still in progress across turns;
- the user explicitly said not to update the wiki.

## Boundaries

Wiki workflows may read source files as evidence, but they must not modify files
outside `wiki/` unless the user explicitly asks for a non-wiki project change.
Host-specific packaging files are source files for this plugin repository and
are not part of a target project's wiki content.
