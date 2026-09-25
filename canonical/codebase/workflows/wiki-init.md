# /wiki-init [wiki-root]

Bootstrap the wiki for this repository. Run once per repo.

Argument:

- `[wiki-root]` is the wiki folder name, for example `wiki`, `.wiki`, or `kb`.
  If omitted, init proposes one in Step 3.

Requires the wiki maintainer skill. Follow `<wiki-root>/SCHEMA.md` if it
exists; otherwise use the default schema.

## Step 0 - Resolve the wiki root

{{include:partials/resolve-wiki-root.md}}

For `/wiki-init`, a `.wikidir` that names a directory that does not
exist is not an error: propose that name in Step 3.

## Step 1 - Check preconditions

- If Step 0 resolved an existing wiki and `<wiki-root>/index.md` exists, stop
  and ask whether to skip, re-init, or run `/wiki-ingest` instead. Re-init
  requires explicit confirmation before deleting or replacing anything.
- If the current directory does not look like a code repo or software project,
  ask for confirmation before proceeding.

## Step 2 - Survey the repo

Do a read-only scan. Do not read every source file yet.

Collect:

1. top-level files and directories;
2. README and architecture/project docs;
3. package manifests and toolchain files;
4. main source directories and entrypoints;
5. tests, CI, build, lint, and deploy signals;
6. config/env/migration/runtime signals;
7. project docs, roadmap, status, proposal, or communication material;
8. existing agent/context/changelog files that should be migrated into
   `<wiki-root>/agent/` if in scope;
9. the wiki root to propose: the `[wiki-root]` argument if given; otherwise
   `.wiki` when `git check-ignore -q .wiki/` succeeds (the repository already
   ignores that folder, as repositories that ignore every `.*` path do);
   otherwise `wiki`.

## Step 3 - Propose the plan

Tell the user:

- the wiki root, `<name>/`, and whether git will track it. Run
  `git check-ignore -q <name>/` (keep the trailing slash so folder-only
  patterns match): success means the wiki stays local and out of shared git
  history; failure means it shows up in `git status` and is committed like
  other project files. If the user wants a local-only wiki that git would
  track, suggest adding `<name>/` to `.git/info/exclude`; do not edit git files
  yourself. When `<name>` is not `wiki`, also run `git check-ignore -q
  .wikidir`, because the pointer must travel with the wiki: for a local-only
  wiki, suggest excluding both `<name>/` and `.wikidir`; for a tracked wiki
  whose `.wikidir` git would ignore, warn that teammates will get the wiki but
  not the pointer, and suggest `wiki` (which needs no pointer) or committing
  the pointer with `git add -f .wikidir`.
- one sentence describing the project;
- which engineering pages will be populated;
- which modules/areas will get module pages;
- which project pages have enough evidence to populate;
- which project-docs pages will be stubs versus evidence-backed pages;
- any legacy docs proposed for later retirement;
- the initial agent context/activity/handoff pages that will be created;
- the initial work tracker page that will be created;
- the portable project overview page name:
  `<wiki-root>/overview-<project-slug>.md`.

Ask: `Proceed with this plan? Adjust anything?`

Wait for confirmation before writing.

Before writing, validate the confirmed name. It must be a single directory
name matching `^\.?[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9_-])?$` (no trailing
dot), and must not be one of `.git`, `.github`, `.claude`, `.codex`, `.agents`,
`.agent`, `.gemini`, `.opencode`, `.obsidian`, `.vscode`, `node_modules`,
`.wikidir`, compared case-insensitively, and must not be an existing directory
that already contains files (unless the user confirmed a re-init of that wiki
in Step 1). If it fails, explain why and ask for another name.

## Step 4 - Create the scaffold

After confirmation:

1. Create `<wiki-root>/` and the default directory tree.
2. If `<wiki-root>` is not `wiki`, write `.wikidir` at the repository root
   containing only the folder name and a newline, for example `.wiki`. This
   is the only file init writes outside `<wiki-root>/`. When `<wiki-root>` is
   `wiki`, do not create `.wikidir`.
3. Copy or adapt the default schema to `<wiki-root>/SCHEMA.md`, replacing each
   `<wiki-root>` placeholder in it with the chosen name.
4. Create pages with frontmatter: `title`, `updated`, `sources`,
   `source_commit` when git is available, and `confidence`.
5. Populate only what is supported by evidence. Use explicit stubs for pages
   that matter but have no verified content yet.

Create at least:

- `<wiki-root>/index.md`
- `<wiki-root>/log.md`
- `<wiki-root>/overview.md`
- `<wiki-root>/overview-<project-slug>.md`
- core `<wiki-root>/engineering/*` pages
- relevant `<wiki-root>/modules/*` pages
- `<wiki-root>/project/status.md` if any project-state evidence exists
- `<wiki-root>/project/work-tracker.md`
- `<wiki-root>/agent/context.md`, `<wiki-root>/agent/activity.md`, `<wiki-root>/agent/handoff.md`
- `<wiki-root>/glossary.md`

## Step 5 - Write engineering pages first

Engineering is authoritative. Populate:

- architecture and data model from code/config/docs;
- development/testing from package scripts, test files, CI, and README;
- operations from deploy/runtime/config evidence;
- troubleshooting only from observed or documented failure modes;
- change-map with "if you need to change X, start here" guidance.

## Step 6 - Write module pages

For each selected module/area, write:

- purpose;
- key files;
- public interface;
- data/control flow;
- invariants;
- how to change this safely;
- verification;
- common failure modes;
- dependencies;
- related tests;
- open risks.

Omit unsupported sections rather than inventing.

## Step 7 - Write project and project-docs pages

Populate `project/` from evidence only. Link risks, requirements, milestones,
and decisions back to engineering pages.

Populate `project-docs/` as reusable communication material only when claims
are supported. Put unsupported but useful future claims in `project-docs/evidence.md`
as gaps or hypotheses.

Also create `<wiki-root>/overview-<project-slug>.md` as the portable project card. The
slug must be lowercase kebab-case. Include:

- what the project is;
- why it exists;
- current status;
- main stack or technical areas;
- milestones or next steps;
- important decisions to remember;
- links to the most relevant wiki pages;
- `## Personal Wiki Export`.

In `## Personal Wiki Export`, write content suitable for import into a
SecondBrain vault under `raw/projects/`. Include project name, short
description, current status, role in the user's work/life, personal motivation
if known, technologies or skills represented, important next steps, and
long-term notes. Do not invent personal meaning; use `Da confermare.` for
unknown personal context.

## Step 8 - Write agent continuity pages

Create `<wiki-root>/agent/context.md` as a fast onboarding page for coding agents. Use
the structure from `references/agent-context-template.md` and include:

- project snapshot;
- architecture or main areas;
- non-negotiable technical rules;
- setup, test, lint, and build commands;
- files to read first;
- risks and invariants;
- links to the most important wiki pages.

Create `<wiki-root>/agent/handoff.md` as a pass-the-baton page. Use the structure from
`references/agent-handoff-template.md` and include git state when available:
branch, last commit, and clean/dirty worktree.

`<wiki-root>/agent/handoff.md` must include:

```markdown
## Baton For Next Coding Agent

| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
```

Every task must have start files, done criteria, and a verification command. If
no concrete task is known, write one row that says `No active coding task` and
mark verification as `Not verified - no active task`.

Create `<wiki-root>/project/work-tracker.md` using
`references/work-tracker-template.md`. Keep it compact and link active work to
`<wiki-root>/agent/handoff.md`.

## Step 9 - Update index and log

Make `index.md` a complete catalog grouped by Overview, Engineering, Modules,
Project, Project Docs, Agent, and Reference.

Append to `log.md`:

```markdown
## [YYYY-MM-DD] init | bootstrapped wiki
- Scope: <one line>
- Wiki root: <wiki-root>/
- Pages created: <count>
- Modules: <list>
- Project/project-docs pages populated: <list or none>
- Agent continuity: context, handoff, activity, work tracker
- Portable overview: overview-<project-slug>.md
- Proposed for retirement: <list or none>
- Follow-up: run /wiki-lint to verify coverage
```

Append the initial entry to `<wiki-root>/agent/activity.md` with agent, trigger,
intent, actions, changed wiki files, validation, decisions, and follow-up.

## Step 10 - Report

Report:

- the wiki root and whether git tracks it;
- what was created;
- what was populated versus left as stubs;
- proposed legacy retirement;
- suggested next step: `/wiki-lint`.

## Guardrails

- Never modify source files during init.
- Never write outside `<wiki-root>/` except `.wikidir`.
- Never delete legacy docs during init.
- If the repo is huge, ask the user to narrow scope.
- Prefer fewer accurate pages over many generic pages.
