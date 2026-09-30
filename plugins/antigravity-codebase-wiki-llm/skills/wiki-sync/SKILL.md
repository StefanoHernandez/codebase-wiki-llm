---
name: wiki-sync
description: Surgically sync existing wiki pages after small source or project changes. Use when the user says /wiki-sync, wiki sync, update wiki from recent changes, or after a completed coding task in a repo that already has a codebase wiki.
---

<!-- Generated from codebase/workflows/wiki-sync.md. Do not edit directly. -->

# /wiki-sync

Fast, surgical wiki update based on small recent changes.

Requires the wiki maintainer skill. Respect `<wiki-root>/SCHEMA.md`.

## Step 0 - Resolve the wiki root

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

## Step 1 - Fast preconditions

- If Step 0 found no wiki, exit silently.
- If no source/config/project files changed, report `wiki-sync: nothing to do.`

## Step 2 - Determine changes

Prefer git:

1. `git status --porcelain` for uncommitted and untracked files.
2. `git diff --name-only HEAD` for working-tree changes.
3. For each wiki page source, `git log <source_commit>..HEAD -- <source>` for
   committed changes since the page was written.

If git is unavailable, use mtimes.

Filter out paths excluded by `<wiki-root>/SCHEMA.md` and `<wiki-root>/` itself.

## Step 3 - Map changes to pages

Locate core pages through SCHEMA `## Core map`. When it is missing (v1 wiki),
use the v1 paths in the maintainer skill and suggest `/wiki-init --adopt <root>`
in the report. A Core map row `activity (v1)` is part of the `log` (not an
orphan) until merged.

For each changed file, find pages whose `sources:` include it or whose prose
references the relevant module/area.

Also map common change types:

- source/API changes -> `modules/*` and the architecture, data-model and
  change-map topic pages listed in SCHEMA `## Topics`;
- tests/CI, setup/tooling, deploy/config/env changes -> the matching topic
  page listed in SCHEMA `## Topics`;
- bugfix/failure-mode changes -> `troubleshooting`;
- roadmap/status/risk docs -> `tracker`, `risks`;
- plan, active work, next task, done criteria, verification state, or blockers
  -> `tracker`, `handoff`;
- architecture decisions, technical commands, risk/invariant changes, or
  read-first file changes -> `context`, `decisions`;
- reusable evidence or demos -> the topic page listed in SCHEMA `## Topics`;
- non-trivial agent work -> `log`, `handoff`, `tracker`.

If more than roughly 10 pages are affected, stop and recommend `/wiki-ingest`
or `/wiki-lint`.

## Step 4 - Update affected existing pages

Apply minimum edits:

- fix factual claims;
- update verification commands or failure modes;
- update frontmatter;
- add supersession notes for corrected claims;
- lower confidence when evidence is incomplete;
- update `context` when project onboarding facts, commands, risks,
  invariants, or high-value links changed;
- `tracker` and `handoff` are updated in Step 6.

Do not create new pages during sync, except files the user confirmed in
Step 7 (decision, log archive), which the agent then writes. If a new page is needed, report the gap and
recommend `/wiki-ingest`.

## Step 5 - Update index only if necessary

Touch `index` only when summaries, titles, or page availability changed.

## Step 6 - Log, tracker, handoff

1. Append one entry to `log` in SCHEMA `## Log format`, author `agent`.
2. Update the status of every touched ID in `tracker`; never write status
   anywhere else.
3. Rewrite `handoff`: last completed step, next tasks (baton table), what not
   to redo, commands already run.

## Step 7 - Proposals (ask, do not write)

- **Decision**: the change adds a dependency, changes architecture, or rejects
  an alternative -> propose `NNNN-<slug>.md` under the `decisions` path (Core map)
  (`references/decision-template.md`).
- **Troubleshooting**: the session solved a non-obvious problem -> propose an
  entry (`references/troubleshooting-template.md`).
- **Log archive**: a phase of the project division closed, or `log` exceeds
  its budget -> propose moving entries up to that date to
  `<phase-or-period>.md` under the `log-archive` path (Core map), leaving one link line. Cut by date:
  phases overlap in time.
- **Verified facts**: a fact in `context` changed -> propose the new value
  with its evidence and date.

## Step 8 - Report briefly

Keep output short:

- `wiki-sync: nothing to do.`
- or `wiki-sync: updated <pages> based on <files>. <follow-up>`

List the proposals made.

## Guardrails

- Never create new pages during sync, except files the user confirmed in
  Step 7 (decision, log archive), which the agent then writes.
- Never delete pages during sync.
- Never touch source code.
- If unsure whether the change is small, do not edit; recommend ingest or lint.
