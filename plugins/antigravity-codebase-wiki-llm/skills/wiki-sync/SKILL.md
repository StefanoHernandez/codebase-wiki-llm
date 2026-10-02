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
- Only after Step 2 established usable change coverage, if no
  source/config/project files changed and the log-archive rule (SCHEMA
  `## Log format`) does not apply, report `wiki-sync: nothing to do.`
  Changed files include uncommitted ones, those committed since the code
  state (`@<short-sha>`) of the latest `log` entry, and those named by a
  `Codebase Wiki LLM (note, not a stop)` line in your context.

## Step 2 - Determine changes

Prefer git:

1. `git status --porcelain` for uncommitted and untracked files.
2. `git diff --name-only HEAD` for working-tree changes.
3. Read SCHEMA `## Log format`: use the latest log's code state only when
   the project permits recording it. Before any revision range, resolve its
   anchor with `git rev-parse --verify --end-of-options '<sha>^{commit}'` and
   establish that it is an ancestor of HEAD (`git merge-base --is-ancestor
   <resolved-commit> HEAD`). Use `git diff --name-only <resolved-commit>..HEAD`
   only for a usable anchor. Add the files named by a
   `Codebase Wiki LLM (note, not a stop)` line regardless of anchor availability.
4. For each wiki page source, validate `source_commit` the same way before
   `git log <resolved-commit>..HEAD -- <source>`. Missing/`unknown`, unresolvable
   or non-ancestor anchors are unavailable baselines, not empty diffs.

If the latest log has no usable baseline (project policy, legacy content or
rewritten history), state `committed-change coverage incomplete` and why.
Use available page baselines, working-tree changes and reminder paths; inspect
current sources for affected pages with no baseline and compare their claims.
Pages without metadata are unanchored; do not assume them current. Report
unmapped or unexamined coverage and recommend `/wiki-lint` or `/wiki-ingest`
for broader recovery. This fallback cannot prove every committed change was
covered and must never yield `wiki-sync: nothing to do.`

If git is unavailable, use mtimes only as signals to inspect current sources
and report incomplete committed-change coverage. Timestamp comparisons alone
do not prove pages current. Apply Step 3's small-change limit to the fallback
too; do not silently expand sync into a full migration.

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

1. Append one entry to `log` in SCHEMA `## Log format`, author `agent`. Preserve
   a project ban on commit hashes: retain the actual command, essential
   output, date and relevant environment, with code state not recorded by
   project policy. Do not invent a replacement digest or insert a hash to
   repair the sync baseline. Report any incomplete change coverage.
2. Update the status of every touched ID in `tracker`; never write status
   anywhere else. Mark 🟢 only when the row's `Done when` criteria are proven
   (proof in `Criteria met` and its source in `Evidence`). Explicit human
   closure without proof moves the row to Done with Status ⚫ and
   `closed by <person> YYYY-MM-DD; not proven: <what>` in `Criteria met`,
   citing the human closure source in `Evidence`; never infer that authority.
   Otherwise keep it Open and name what is missing. New work the change
   suggests goes to `## Proposals`.
   This rule governs current work and new completion claims. Do not reclassify
   unresolved historical terminal rows encountered during unrelated sync:
   preserve them, report missing proof/authority for human resolution, and
   keep the validation gap explicit. Adoption's column normalization alone
   never supplies that resolution.
3. Rewrite `handoff`: `Tracker IDs`, last completed step, next tasks (baton
   table with tracker IDs), what not to redo, commands already run and Git
   state. Activity status remains in the tracker.
4. Archive the log without asking when the SCHEMA `## Log format` rule
   applies. When a phase of the project division closed, move the entries
   dated up to its closing date that are still in `log` to `<phase>.md`. When
   `log` is over its budget, move whole calendar months, oldest first, to
   `<YYYY-MM>.md` until it fits, always keeping at least the last 10 entries.
   Both go under the `log-archive` path (Core map). At the first actual archive
   write, validate that this path stays inside the wiki and is not blocked by
   a file or dangling symlink, then create its missing directories. Entries move unchanged
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
