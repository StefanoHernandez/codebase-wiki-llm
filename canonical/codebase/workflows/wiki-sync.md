# /wiki-sync

Fast, surgical wiki update based on small recent changes.

Requires the wiki maintainer skill. Respect `<wiki-root>/SCHEMA.md`.

## Step 0 - Resolve the wiki root

{{include:partials/resolve-wiki-root.md}}

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
- `context` Verified Facts: when this change brings new evidence for a fact,
  update its value, evidence, date and code state directly. When a fact's
  evidence source changed and the fact cannot be re-proved now, replace its
  Verified date with `⚠️ TO RE-VERIFY (<what changed>)`; never keep the old
  date and never delete the row silently;
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
- **Troubleshooting**: the session solved a non-obvious or recurring problem -> propose an
  entry (`references/troubleshooting-template.md`).
- **Log archive**: a phase of the project division closed, or `log` exceeds
  its budget -> propose moving entries up to that date to
  `<phase-or-period>.md` under the `log-archive` path (Core map), leaving one link line. Cut by date:
  phases overlap in time.

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
