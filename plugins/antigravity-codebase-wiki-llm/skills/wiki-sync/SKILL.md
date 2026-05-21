---
name: wiki-sync
description: Surgically sync existing wiki pages after small source or project changes. Use when the user says /wiki-sync, wiki sync, update wiki from recent changes, or after a completed coding task in a repo that already has wiki/.
---

<!-- Generated from codebase/workflows/wiki-sync.md. Do not edit directly. -->

# /wiki-sync

Fast, surgical wiki update based on small recent changes.

Requires the wiki maintainer skill. Respect `wiki/SCHEMA.md`.

## Step 1 - Fast preconditions

- If `wiki/` does not exist, exit silently.
- If no source/config/project files changed, report `wiki-sync: nothing to do.`

## Step 2 - Determine changes

Prefer git:

1. `git status --porcelain` for uncommitted and untracked files.
2. `git diff --name-only HEAD` for working-tree changes.
3. For each wiki page source, `git log <source_commit>..HEAD -- <source>` for
   committed changes since the page was written.

If git is unavailable, use mtimes.

Filter out paths excluded by `wiki/SCHEMA.md` and `wiki/` itself.

## Step 3 - Map changes to pages

For each changed file, find pages whose `sources:` include it or whose prose
references the relevant module/area.

Also map common change types:

- source/API changes -> `modules/*`, `engineering/architecture.md`,
  `engineering/data-model.md`, `engineering/change-map.md`;
- tests/CI changes -> `engineering/testing.md`;
- setup/tooling changes -> `engineering/development.md`;
- deploy/config/env changes -> `engineering/operations.md`;
- bugfix/failure-mode changes -> `engineering/troubleshooting.md`;
- roadmap/status/risk docs -> `project/*`;
- reusable evidence or demos -> `project-docs/evidence.md`,
  `project-docs/demo-materials.md`;
- non-trivial agent work -> `agent/activity.md`, `agent/handoff.md`.

If more than roughly 10 pages are affected, stop and recommend `/wiki-ingest`
or `/wiki-lint`.

## Step 4 - Update affected existing pages

Apply minimum edits:

- fix factual claims;
- update verification commands or failure modes;
- update frontmatter;
- add supersession notes for corrected claims;
- lower confidence when evidence is incomplete.

Do not create new pages during sync. If a new page is needed, report the gap and
recommend `/wiki-ingest`.

## Step 5 - Update index only if necessary

Touch `index.md` only when summaries, titles, or page availability changed.

## Step 6 - Append log/activity

Append to `log.md`:

```markdown
## [YYYY-MM-DD] sync | <N> pages updated
- Changed files: <short list or count>
- Pages updated: <list>
- Follow-ups: <none or recommended ingest/lint>
```

Append to `agent/activity.md` if the sync closes a non-trivial task or records a
decision useful to future agents.

## Step 7 - Report briefly

Keep output short:

- `wiki-sync: nothing to do.`
- or `wiki-sync: updated <pages> based on <files>. <follow-up>`

## Guardrails

- Never create new pages during sync.
- Never delete pages during sync.
- Never touch source code.
- If unsure whether the change is small, do not edit; recommend ingest or lint.
