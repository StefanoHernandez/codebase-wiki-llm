# /wiki-sync

Fast, surgical wiki update based on small recent changes.

Requires the wiki maintainer skill. Respect `<wiki-root>/SCHEMA.md`.

## Step 0 - Resolve the wiki root

{{include:partials/resolve-wiki-root.md}}

## Step 1 - Fast preconditions

- If Step 0 found no wiki, exit silently.
- If no source/config/project files changed and the log-archive rule (SCHEMA
  `## Log format`) does not apply, report `wiki-sync: nothing to do.`
  Changed files include uncommitted ones, those committed since the code
  state (`@<short-sha>`) of the latest `log` entry, and those named by a
  `Codebase Wiki LLM (note, not a stop)` line in your context.

## Step 2 - Determine changes

Prefer git:

1. `git status --porcelain` for uncommitted and untracked files.
2. `git diff --name-only HEAD` for working-tree changes.
3. `git diff --name-only <sha>..HEAD`, where `<sha>` is the code state of the
   latest `log` entry, for work committed since the last sync; add the files
   named by a `Codebase Wiki LLM (note, not a stop)` line.
4. For each wiki page source, `git log <source_commit>..HEAD -- <source>` for
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

Do not create new pages during sync, except log archives (Step 6) and decision
records (Step 7). If another new page is needed, report the gap and recommend
`/wiki-ingest`.

## Step 5 - Update index only if necessary

Touch `index` only when summaries, titles, or page availability changed.

## Step 6 - Log, tracker, handoff

1. Append one entry to `log` in SCHEMA `## Log format`, author `agent`.
2. Update the status of every touched ID in `tracker`; never write status
   anywhere else. Mark 🟢 only when the row's `Done when` criteria are proven
   (proof in `Criteria met` and its source in `Evidence`). Explicit human
   closure without proof moves the row to Done with Status ⚫ and
   `closed by <person> YYYY-MM-DD; not proven: <what>` in `Criteria met`,
   citing the human closure source in `Evidence`; never infer that authority.
   Otherwise keep it Open and name what is missing. New work the change
   suggests goes to `## Proposals`.
3. Rewrite `handoff`: `Tracker IDs`, last completed step, next tasks (baton
   table with tracker IDs), what not to redo, commands already run and Git
   state. Activity status remains in the tracker.
4. Archive the log without asking when the SCHEMA `## Log format` rule
   applies. When a phase of the project division closed, move the entries
   dated up to its closing date that are still in `log` to `<phase>.md`. When
   `log` is over its budget, move whole calendar months, oldest first, to
   `<YYYY-MM>.md` until it fits, always keeping at least the last 10 entries.
   Both go under the `log-archive` path (Core map). Entries move unchanged
   (dates, evidence and links kept; relative links rewritten only so they
   still resolve); an existing archive file is appended to, never replaced;
   `log` keeps one link line per archive. The fixed names and cuts make
   archives written on parallel branches match. Make it one self-contained
   edit; when git does not track the wiki, list the moved date range in the
   report, since git cannot undo it.

## Step 7 - Decisions and unresolved proposals

- **Already approved decision**: when the change implements a recorded human
  choice or approval documented in the project's process, create or update
  `NNNN-<slug>.md` under the `decisions` path (Core map) as `accepted` using
  `references/decision-template.md`. Record who approved it, where and when
  under `## Approval`; documenting that authority needs no repeat permission.
- **Unresolved decision**: when the change suggests a new dependency,
  architecture choice or alternative, record the idea as `proposed` with who
  proposed it and when, and ask only for the unresolved choice. Never infer
  approval from implementation, invent reasons or rejected alternatives.
- Resolve source placeholders to concrete repository-relative paths before
  writing decision records, and update the mapped `index` for any new record.
- **Troubleshooting**: the session solved a non-obvious or recurring problem -> propose an
  entry (`references/troubleshooting-template.md`).

## Step 8 - Report briefly

Keep output short:

- `wiki-sync: nothing to do.`
- or `wiki-sync: updated <pages> based on <files>. <follow-up>`

List the proposals made and any log archive (file, entry count, date range).

## Guardrails

- Never create new pages during sync, except log archives (Step 6) and decision
  records (Step 7).
- Never delete pages during sync.
- Never touch source code.
- If unsure whether the change is small, do not edit; recommend ingest or lint.
