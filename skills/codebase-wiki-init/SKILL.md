---
name: codebase-wiki-init
description: Bootstrap an engineering-first software project wiki in wiki/, .wiki/, or a folder you choose.
---

<!-- Generated from codebase/workflows/wiki-init.md. Do not edit directly. -->

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

For `/wiki-init`, a `.wikidir` that names a directory that does not
exist is not an error: propose that name in Step 3.

## Step 1 - Check preconditions

- If Step 0 resolved a wiki whose `SCHEMA.md` has a `## Core map`, stop and ask
  whether to skip, re-init, run `/wiki-ingest`, or install/repair the
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

## Step 3 - One message with numbered proposals

Send one message. Pre-fill every answer from the survey. Reply `ok` accepts
all; `3: releases, 5: yes` overrides by number.

1. **Folder** - adopt `<folder>` (N pages found) · new `wiki` · new `.wiki`
   (propose `.wiki` when `git check-ignore -q .wiki/` succeeds).
2. **Language** - from the README.
3. **Project division** - phases/WP · releases · sprints/milestones · none.
4. **Topics** - pre-checked list from the survey; `architecture` checked for
   any repo with more than one source directory.
5. **Sensitive data** - default `no` · yes (then ask for forbidden terms and local-only
   paths in the same reply).
6. **Agent entry file** - create a thin `CLAUDE.md`/`AGENTS.md` pointing to
   the context page · none. An existing file is never overwritten: propose
   only removing status it duplicates.

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
  replacing each `<wiki-root>` placeholder with the folder name. If it already
  has one (v1 wikis included), keep it: add the missing v2 sections (`## Project
  profile`, `## Core map`, `## Conventions`, `## Budgets`, `## Topics`,
  `## Evidence`, `## Confidentiality`, `## Log format`) and preserve existing
  content. If an existing section conflicts with a v2 one, show both and ask.
  Never replace an existing `SCHEMA.md` wholesale.
- Fill `## Project profile` (language, project division, sensitive data, agent
  entry file) and `## Topics` from the answers confirmed in Step 3.
- Fill `## Core map` with the existing files that play each role (e.g. an
  existing project log → `log`, an `adr/` folder → `decisions`). For a v1 wiki
  map `agent/activity.md` under a row `activity (v1)` and propose merging it
  into the log.
- List core roles with no existing file and propose creating only those.
- Never move, rename or delete files without confirmation.

## Step 5 - New wiki

Write `SCHEMA.md` from the default schema (replacing each `<wiki-root>`
placeholder with the folder name) and fill `## Project profile` and
`## Topics` from the answers confirmed in Step 3, as in Step 4. Create the
core pages at the default Core map paths and the confirmed topics.
Populate only what the survey supports; everything else is an explicit stub.
`context` follows `references/agent-context-template.md`; `handoff` follows
`references/agent-handoff-template.md`; `tracker` follows
`references/work-tracker-template.md`.

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

## Step 7 - Log and report

Append the first log entry (SCHEMA `## Log format`) to the Core map `log`
path (in adopt mode, created in Step 4 if that role was missing), then report: wiki root,
adopted or created pages, stubs, files changed outside the wiki.

## Guardrails

- Never modify source files during init.
- Never delete or move existing docs without confirmation.
- If the repo is huge, ask the user to narrow scope.
