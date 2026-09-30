---
name: codebase-wiki-context
description: Use when a repository has a codebase wiki (wiki/, or the folder named in .wikidir) and coding work should read it and keep the log, work tracker, and handoff current.
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

Read `<wiki-root>/SCHEMA.md` first and find every page below through its
`## Core map`. If SCHEMA has no `## Core map`, use the maintainer skill's v1 paths.

When the conversation has no wiki context yet (a new chat, a cleared or
compacted context, or a session line `Codebase Wiki LLM: new context`), read
the core once, before the first task, skipping pages the conversation already
holds:

1. `index`: the catalog.
2. `context`: its `Verified Facts` are not re-derived.
3. `handoff`: if the session context says the handoff is N commits old, say
   which handoff items no longer match the repo and refresh it before continuing.
4. `tracker`; the latest `log` entries (since the handoff's `updated` date, at
   most the last 10); `risks`; `troubleshooting`; `glossary`; the titles of the
   `decisions` files.

Later turns of the same conversation read only the pages the task needs.
Prefer wiki pages over re-reading source when they cover the topic; verify the
source when accuracy matters, confidence is low, or a fact is marked
`⚠️ TO RE-VERIFY`.

If the wiki cannot answer, read source or project documents. If that reveals
durable knowledge, mention the gap or run `/wiki-ingest` when asked.

## After completing a non-trivial task

A context line starting `Codebase Wiki LLM (note, not a stop)` means earlier
work changed code the wiki does not cover yet. Handle the user's message
first; when that earlier work is done, run `/wiki-sync`, or say in one line
why no wiki update is needed.

If source/config/project files changed and `<wiki-root>/` exists:

1. Run `/wiki-sync` unless the user opted out. It writes the `log` entry and
   updates `tracker` and `handoff`.
2. If you did not run it, append the `log` entry (SCHEMA `## Log format`) and
   update `tracker`/`handoff` yourself when the task changed project state, the
   plan, decisions or blockers, ran significant verification, or left work
   incomplete.
3. Update `context` when architecture, commands, invariants, risks or read-first
   files changed.
4. Every claim you write follows SCHEMA `## Evidence`, in proportion to the
   claim: a verification carries command, essential output, date and code state
   (`@<short-sha>`); what you could not check is `> ⚠️ NOT VERIFIED - <reason>`.

Do not run `/wiki-sync` when no source/config/project files changed, the task is
still in progress across turns, or the user said not to update the wiki.

## Boundaries

- Do not modify files outside `<wiki-root>/` unless the user explicitly asks for a
  non-wiki project change; source files are read-only evidence.
- Never write a term listed in `<wiki-root>/.private-terms` outside that file.
- Host-specific packaging files are not part of a target project's wiki content.
