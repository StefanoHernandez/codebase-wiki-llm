# /wiki-init [wiki-root] [--adopt <folder>]

Bootstrap the wiki for this repository. Run once per repo.

Arguments:

- `[wiki-root]` is the wiki folder name, for example `wiki`, `.wiki`, or `kb`.
  If omitted, init proposes one in Step 3.
- `--adopt <folder>` adopts an existing documentation folder as the wiki
  instead of creating a new one (Step 4).

Requires the wiki maintainer skill. Follow `<wiki-root>/SCHEMA.md` if it
exists; otherwise use the default schema.

## Step 0 - Resolve the wiki root

{{include:partials/resolve-wiki-root.md}}

For `/wiki-init`, a `.wikidir` that names a directory that does not
exist is not an error: propose that name in Step 3.

## Step 1 - Check preconditions

- An explicit `--adopt <folder>` also works when that wiki already has a Core
  map: continue with the read-only survey and scoped compatibility recovery,
  preserving its paths and content. This is not scaffold re-initialization.
- Otherwise, if Step 0 resolved a wiki whose `SCHEMA.md` has a `## Core map`, stop and ask
  whether to skip, use `--adopt` for compatibility recovery, re-init, run `/wiki-ingest`, or install/repair the
  forbidden-terms hook only (the hook part of Step 6, nothing else). Re-init
  rebuilds the scaffold after explicit confirmation; existing pages are never
  deleted, only proposed for replacement one by one.
- If Step 0 resolved a wiki whose `SCHEMA.md` has no `## Core map`, it is a v1
  wiki: continue in adopt mode on that folder (Step 4).
- If the current directory does not look like a code repo or software project,
  ask for confirmation before proceeding.

## Step 2 - Survey (read-only)

Collect: top-level layout; existing documentation folders (`docs`, `wiki`,
`documentation`) and their Markdown page count; `CLAUDE.md` / `AGENTS.md`;
README language; manifests, tests, CI, build and deploy signals; `.gitignore`.
Do not read every source file.

For adoption, inventory missing page frontmatter, the actual tracker columns,
and explicit project rules in existing docs (especially the log). Counting
metadata gaps does not verify the old content. Keep these findings for the
scope proposal; a numbered layout is not a compatibility problem.

## Step 3 - One message with numbered proposals

Send one message. Pre-fill every answer from the survey. Reply `ok` accepts
all; `3: releases, 5: yes` overrides by number.

1. **Folder** - adopt `<folder>` (N pages found) · new `wiki` · new `.wiki`
   (propose `.wiki` when `git check-ignore -q .wiki/` succeeds).
2. **Language** - for headings and prose; proposed from the README or, when
   docs or a wiki already exist, from them. Asked in every init, adopt mode
   included.
3. **Project division** - phases/WP · releases · sprints/milestones · none.
4. **Topics** - pre-checked list from the survey; `architecture` checked for
   any repo with more than one source directory.
5. **Sensitive data** - default `no` · yes (then ask for forbidden terms and local-only
   paths in the same reply).
6. **Agent entry file** - create a thin `CLAUDE.md`/`AGENTS.md` pointing to
   the context page · none. An existing file is never overwritten: propose
   only removing status it duplicates.
7. **Parallel work** - add `<wiki-root>/<log path> merge=union` to
   `.gitattributes`, so log entries written in parallel merge without
   conflicts · no. Default yes when git tracks the wiki, no for a local-only
   wiki.

For adoption, include a compatibility plan within proposal 1: the number of
pages missing metadata, the tracker columns before and after normalization,
and local rules the schema will retain. Propose gradual metadata recovery:
new and substantively updated pages get supported metadata; untouched pages
and marker-only edits remain listed as gaps. Full recovery is an alternative
only when the user chooses it. Show which existing tracker rows lack criteria,
verification or closure evidence; normalization preserves their content and
IDs, and leaves missing values explicit. Scope approval covers only the edits
shown; do not treat adoption as approval to verify or rewrite all old pages.

Show conventions and budgets as defaults from SCHEMA; do not ask about them.
Also state whether git will track the folder: run `git check-ignore -q
<name>/` (keep the trailing slash); success means it stays local. If the user
wants a local-only wiki that git would track, suggest adding `<name>/` to
`.git/info/exclude`; init itself writes `.git/info/exclude` only in Step 6,
for local-only paths whose names contain a forbidden term. When `<name>` is not
`wiki`, also run `git check-ignore -q .wikidir`: for a local-only wiki suggest
excluding both; for a tracked wiki whose `.wikidir` git would ignore, warn that
teammates will get the wiki but not the pointer, and suggest `wiki` or
`git add -f .wikidir`.

Wait for the reply before writing.

Before writing, validate the confirmed folder name. It must be a single
directory name matching `^\.?[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9_-])?$` (no
trailing dot) and must not be one of `.git`, `.github`, `.claude`, `.codex`,
`.agents`, `.agent`, `.gemini`, `.opencode`, `.obsidian`, `.vscode`,
`node_modules`, `.wikidir`, compared case-insensitively. A new (non-adopted)
folder that already exists with files is not allowed: propose adopt mode
instead. If validation fails, explain why and ask for another name.

## Step 4 - Adopt mode

Used for option 1 "adopt", for `--adopt <folder>`, and for v1 wikis.

- `.wikidir` is written in Step 6.
- If the folder has no `SCHEMA.md`, write one from the default schema,
  replacing each `<wiki-root>` placeholder with the folder name and carrying
  forward the explicit project rules found in Step 2. For example, a rule
  forbidding hashes in the log changes `## Log format`, not automatically
  page `source_commit` policy. If it already
  has one (v1 wikis included), keep it: add the missing v2 sections (`## Project
  profile`, `## Core map`, `## Conventions`, `## Budgets`, `## Topics`,
  `## Evidence`, `## Confidentiality`, `## Log format`) and preserve existing
  content. If an existing section conflicts with a v2 one, show both and ask.
  Never replace an existing `SCHEMA.md` wholesale.
- Apply the compatibility edits confirmed in Step 3. If a newly discovered
  conflict requires different edits, propose those before changing the
  affected content. Keep metadata recovery scoped: actual evidence paths
  must support the page's claims, not merely appear among its links. A new
  metadata date or current commit never proves old prose; use `unknown` for
  an unestablished source baseline and assess confidence from evidence.
  When no supporting sources are established, retain the page as a reported
  metadata gap rather than manufacture a source list.
- Normalize confirmed tracker tables to the template columns, retaining
  all original information. Translated tables keep the documented column
  order; retain extra data in labeled notes associated with the same IDs.
  Split grouped IDs
  only as an approved mapping preserving their original meaning and evidence.
  Move annotations out of date cells without inventing dates or proof. Never
  infer a human closure, convert an unproven historical row to 🟢/⚫, or reopen
  it solely to satisfy validation. Report unresolved status or authority for
  human resolution; incomplete rows remain validation findings.
- Fill `## Project profile` (language, project division, sensitive data, agent
  entry file) and `## Topics` from the answers confirmed in Step 3.
- Fill `## Core map` with the existing files that play each role (e.g. an
  existing project log → `log`, an `adr/` folder → `decisions`). For a v1 wiki
  map `agent/activity.md` under a row `activity (v1)` and propose merging it
  into the log.
- List core roles with no existing file and propose creating only those,
  using the templates and source substitutions in Step 5.
- `log-archive` is a reserved directory path inside the wiki. It need not
  exist until the first archive write; do not create an empty directory or
  `.gitkeep` solely for validation.
- Insert the missing section markers (SCHEMA `## Conventions`) on the line
  under the matching headings of the adopted `context`, `handoff` and
  `tracker` pages; these one-line edits stay inside the wiki. List them in the
  report.
- Never move, rename or delete files without confirmation.
- Migration plan: if the user already declined moves or asked to preserve the
  layout, record the skipped moves without asking again. Otherwise, once the
  Core map works in place, propose moving adopted
  files toward the default layout, as one numbered message: one line per move
  (`<from> → <to>`, why) and the links each move rewrites, plus the files
  outside the wiki that reference `<from>` (`git grep -l`), which it does not
  rewrite. Splitting a v1 `project/decisions.md` into one file per decision is
  a move too. Reply `ok` accepts all; `2: no` skips one. For each accepted
  move: `git mv` when git tracks the file (plain move otherwise), rewrite
  relative links in every wiki page, update the Core map row. Never move a
  file outside `<wiki-root>/`.
  Skipped moves stay mapped where they are; structural adoption requires no
  moves. It does not mean old pages or unresolved tracker rows are validated.

## Step 5 - New wiki

Write `SCHEMA.md` from the default schema (replacing each `<wiki-root>`
placeholder with the folder name) and fill `## Project profile` and
`## Topics` from the answers confirmed in Step 3, as in Step 4. Create the
core pages at the default Core map paths and the confirmed topics.
Populate only what the survey supports; everything else is an explicit stub.
`context` follows `references/agent-context-template.md`; `handoff` follows
`references/agent-handoff-template.md`; `tracker` follows
`references/work-tracker-template.md`.

Before writing any new or adopted content page from a template (including a
decision record), resolve `sources:` placeholders: `<wiki-root>` is the
confirmed folder, `<Core map index path>`, `<Core map log path>`,
`<Core map tracker path>` and `<Core map handoff path>` come from the resolved
Core map, and `<source-path>` is an actual supporting repository-relative
file or directory path from the survey. Use adopted paths, not default paths.
Write one entry per source; never leave a placeholder or a descriptive phrase
as a source. Include a path only when it exists by the end of init; omit
unsupported optional source slots rather than assuming `README.md` exists.
Mapped wiki pages may be sources when they support the content. If there is
no source evidence, keep the content an explicit gap instead of inventing a
path or a claim. For new content, fill `source_commit` with the current short
SHA, or `unknown` when git is unavailable. Retained old prose with no
established baseline uses `unknown`, even when git exists. SCHEMA is
configuration and does not require `sources:`.

## Step 6 - Configuration outside the wiki (confirmed in Step 3 or Step 1 only)

- `.wikidir` when the folder is not `wiki`.
- Sensitive data `yes`: write `<wiki-root>/.private-terms` (one term per line)
  and add `<wiki-root>/.private-terms` and each local-only path to
  `.gitignore`, except local-only paths whose names contain a forbidden term:
  those go into `.git/info/exclude`, which is never committed. Verify with
  `git check-ignore -v`. If it does not confirm that `.private-terms` and each
  local-only path are ignored, stop, report, and do not install the hook.
- Hook (Sensitive data `yes`, or the hook-only option of Step 1). The hooks
  folder is `$(git rev-parse --git-path hooks)` (it honours linked worktrees).
  If `git config core.hooksPath` is set, a hook manager is in use: install
  nothing; show the call line below and tell the user to add it, with the
  script, to their hook manager. Otherwise
  copy the maintainer skill's `scripts/check-private-terms.sh` to
  `$(git rev-parse --git-path hooks)/pre-commit` (`chmod +x`). If a
  pre-commit hook already exists, do not overwrite it: copy the script to
  `$(git rev-parse --git-path hooks)/check-private-terms.sh` (`chmod +x`)
  instead and show this call line to add to the existing hook:
  `sh "$(git rev-parse --git-path hooks)/check-private-terms.sh" || exit 1`
- Agent entry file: at most 15 lines - the non-negotiable rules that must be
  seen before anything else, and a link to the context page.
- `.gitattributes` (item 7 confirmed): append the line
  `<wiki-root>/<log path> merge=union` (Core map `log` path) unless it is
  already there; create the file if missing.

## Step 7 - Log and report

Append the first log entry (SCHEMA `## Log format`) to the Core map `log`
path (in adopt mode, created in Step 4 if that role was missing), then report: wiki root,
adopted or created pages, migration moves done and skipped, stubs, files changed outside the wiki.

In adopt mode, also report metadata gaps (count and paths), unresolved tracker
fields and local conventions retained. Distinguish `structure adopted` from
`structural validation passed`; deferred recovery is never a validator pass.
If Python 3.10+ is available, run the installed maintainer's
`scripts/validate-wiki.py` using the same invocation as `/wiki-lint` and report
its actual exit status. Otherwise state that validation was not run. Do not
fix deferred pages implicitly to obtain a green result.

## Guardrails

- Never modify source files during init.
- Never delete or move existing docs without confirmation.
- If the repo is huge, ask the user to narrow scope.
