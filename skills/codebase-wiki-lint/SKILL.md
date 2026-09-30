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
3. the `index` page;
4. current in-scope source/config/project files;
5. git status and recent commits;
6. root-level legacy docs listed by the schema;
7. SCHEMA `## Project profile` and `## Budgets`;
8. `.private-terms` (existence only, never its content), `.gitignore`, and
   `.git/hooks/`;
9. file sizes from `wc -c`.

Do targeted source reads only where needed to verify claims.

## Step 3 - Checks

Find pages by Core map role (`index`, `log`, `log-archive`, `tracker`,
`decisions`, `risks`, `context`, `handoff`, `troubleshooting`, `glossary`) or
from the topic pages listed in SCHEMA `## Topics`.

### Core map

Flag roles pointing to missing files and broken relative links. A SCHEMA
without `## Core map` is a v1 wiki (old `overview.md`, `agent/`, `project/`
layout): suggest `/wiki-init --adopt <root>`.

### Staleness

Flag pages when:

- `updated` is older than schema policy and sources changed;
- five or more commits touched listed sources since `source_commit`;
- confidence is `low`;
- listed sources are missing.

### Drift

Flag claims contradicted by code, tests, configs, CI, or current project docs.

### Orphans

Flag pages not linked from `index` or another useful page. Ignore `index`,
`SCHEMA.md`, `log`, and `log-archive`.

### Gaps

Flag important source areas, public interfaces, tests, config, operations,
project state, or handoff context that should be documented but is not.

### Engineering quality

Flag module pages missing important sections such as invariants, safe-change
guidance, verification, related tests, or failure modes when evidence exists.

Flag `context` when it lacks a project snapshot, main areas, non-negotiable
rules, setup/test/lint/build commands when evidence exists, files to read
first, or links to important pages.

### Evidence

Apply SCHEMA `## Evidence`. Flag technical claims and `Verified Facts` rows
with no date or no command, and command output with no command. Flag example output placed next to real
output.

### Verified facts

Flag `Verified Facts` rows whose evidence sources changed after the verification date
(`git log --since=<date> -- <source>`).

### Single status

Flag status icons outside `tracker` (except pages that declare another
meaning at the top), IDs cited but missing from `tracker`, duplicated IDs,
and IDs reused for a different task.

Flag `tracker` rows without status, evidence, or next verification.

### Handoff

Flag `handoff` when five or more commits happened since it last changed.

Flag `handoff` when it lacks current work state, last completed step, a
baton for the next agent, prioritized next tasks, blockers and risks,
commands already run with results, work not to redo, or (when git is
available) branch, last commit, and worktree state. Flag baton tasks lacking
start files, done criteria, a verification command or
`Not verified - <reason>`, or notes when blocked or risky.

Flag claims about project state, git state, completed work, verification, or
sources that are not supported by source files, command results, git data, or
linked pages.

### Budget

Measure with `wc -c`. Thresholds come from SCHEMA `## Budgets`; the
per-session read set is the agent entry file (CLAUDE.md/AGENTS.md if present),
`index`, `context`, `handoff`, `tracker`, and `log`; a closed phase is judged
from the project division in SCHEMA `## Project profile`. Flag any page over the single-page budget; the
per-session read set over its budget (list each file's size); `log` over its
budget or holding entries of a closed phase. Suggest the split or the archive
cut.

### Confidentiality

Read `Sensitive data` from SCHEMA `## Project profile`. When it is `no`, skip
this section silently. When it is `yes`:

- run the maintainer skill's `scripts/check-private-terms.sh --all` and
  report its `file:line` output (never print the terms);
- flag a missing `.private-terms`;
- flag local-only paths that `git check-ignore -q` does not ignore;
- flag a missing pre-commit check. It is installed only when EITHER
  `.git/hooks/pre-commit` is the forbidden-terms script
  (`grep -q "private-terms" .git/hooks/pre-commit` and it contains the usage
  string `check-private-terms.sh [--staged|--all]`), OR
  `.git/hooks/check-private-terms.sh` exists AND
  `grep -q check-private-terms.sh .git/hooks/pre-commit` succeeds. Flag
  everything else (no hook, an unrelated pre-commit without the call line, the
  script present but never called) and suggest in the report that `/wiki-init`
  can install it; do not install it.

### Contradictions

Flag disagreements across topic pages, `decisions`, `risks`, `context`,
`tracker`, and source evidence.

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
- Core map: <n>
- Stale: <n>
- Drift: <n>
- Orphans: <n>
- Gaps: <n>
- Engineering quality: <n>
- Evidence: <n>
- Verified facts: <n>
- Single status: <n>
- Handoff: <n>
- Budget: <n>
- Confidentiality: <n>
- Contradictions: <n>
- Legacy: <n>
- Frontmatter: <n>

| Scope | File | Size | Limit |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Findings
...

## Suggested follow-ups
...
```

## Step 5 - Read-only by default

Do not edit the wiki during lint. If the user explicitly asks to save the
report, write it under `<wiki-root>/lint-reports/` and append to the `log` page.

## Guardrails

- Do not modify source files.
- Do not delete or move legacy docs.
- If there are zero issues, say so plainly.
