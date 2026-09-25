---
name: codebase-wiki-lint
description: Run a read-only health check for staleness, drift, gaps, and unsupported claims.
---

<!-- Generated from codebase/workflows/wiki-lint.md. Do not edit directly. -->

# /wiki-lint

Read-only health check for the repository-local wiki.

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

## Step 1 - Preconditions

- If Step 0 found no wiki, tell the user to run `/wiki-init` first.
- Prefer git over mtimes when available.

## Step 2 - Gather facts

Read:

1. every wiki page frontmatter;
2. `<wiki-root>/SCHEMA.md`;
3. `<wiki-root>/index.md`;
4. current in-scope source/config/project files;
5. git status and recent commits;
6. root-level legacy docs listed by the schema.

Do targeted source reads only where needed to verify claims.

## Step 3 - Checks

### Staleness

Flag pages when:

- `updated` is older than schema policy and sources changed;
- five or more commits touched listed sources since `source_commit`;
- confidence is `low`;
- listed sources are missing.

### Drift

Flag claims contradicted by code, tests, configs, CI, or current project docs.

### Orphans

Flag pages not linked from `index.md` or another useful page. Ignore
`index.md`, `SCHEMA.md`, and append-only logs.

### Gaps

Flag important source areas, public interfaces, tests, config, operations,
project state, or agent handoff context that should be documented but is not.

### Engineering quality

Flag module pages missing important sections such as invariants, safe-change
guidance, verification, related tests, or failure modes when evidence exists.

### Project consistency

Flag roadmap/status/risk/requirement claims that are unsupported by project or
engineering evidence.

### Project-docs support

Flag communication claims that lack links to engineering, project, or source
evidence.

### Portable overview

Flag missing `<wiki-root>/overview-<project-slug>.md`.

Flag portable overview pages that:

- do not use lowercase kebab-case in the filename;
- lack `## Personal Wiki Export`;
- lack current status, technical areas, next steps, important decisions, or
  links to relevant technical wiki pages when evidence exists;
- contain personal motivation, career meaning, subjective importance, or user
  priorities that are not sourced or marked `Da confermare.`;
- contradict `overview.md`, `project/status.md`, `project/decisions.md`,
  engineering pages, or source evidence.

### Agent continuity

Flag missing `<wiki-root>/agent/context.md`, `<wiki-root>/agent/activity.md`, or
`<wiki-root>/agent/handoff.md`.

Flag `<wiki-root>/agent/context.md` when it is too generic or lacks:

- project snapshot;
- architecture or main areas;
- non-negotiable technical rules;
- setup, test, lint, or build commands when evidence exists;
- files to read first;
- risks or invariants;
- links to important wiki pages.

Flag `<wiki-root>/agent/handoff.md` when it lacks:

- current work state;
- last completed step;
- `## Baton For Next Coding Agent`;
- prioritized next tasks;
- blockers and risks;
- commands already run and results;
- work not to redo;
- git branch, last commit, and worktree state when git is available.

Flag baton rows when any task lacks:

- start files;
- done criteria;
- verification command or `Not verified - <reason>`;
- notes/blockers when the task is blocked or risky.

Flag stale activity when source/config/project/wiki changes are visible but
`<wiki-root>/agent/activity.md` has no recent entry describing agent, trigger, intent,
actions, changed files, validation, decisions, and follow-up.

Flag claims about project state, git state, completed work, verification, or
sources when they are not supported by source files, command results, git data,
or linked wiki pages.

### Work tracker

Flag missing `<wiki-root>/project/work-tracker.md`.

Flag work tracker rows that have no status, evidence, next verification, or
connection to `<wiki-root>/agent/handoff.md` for active coding work.

### Contradictions

Flag disagreements across overview, engineering, modules, project,
project-docs, and source evidence.

### Legacy docs

For root-level legacy docs, propose retirement only when content is absorbed.
Never delete.

### Frontmatter hygiene

Flag missing fields, invalid dates, invalid confidence, and missing source
files.

## Step 4 - Report

Produce a concise markdown report:

```markdown
# Wiki Lint Report - YYYY-MM-DD

## Summary
<N> issues across <M> pages.
- Stale: <n>
- Drift: <n>
- Orphans: <n>
- Gaps: <n>
- Engineering quality: <n>
- Project consistency: <n>
- Project-docs support: <n>
- Portable overview: <n>
- Agent continuity: <n>
- Work tracker: <n>
- Contradictions: <n>
- Legacy: <n>
- Frontmatter: <n>

## Findings
...

## Suggested follow-ups
...
```

## Step 5 - Read-only by default

Do not edit the wiki during lint. If the user explicitly asks to save the
report, write it under `<wiki-root>/lint-reports/` and append to `<wiki-root>/log.md`.

## Guardrails

- Do not modify source files.
- Do not delete or move legacy docs.
- If there are zero issues, say so plainly.
