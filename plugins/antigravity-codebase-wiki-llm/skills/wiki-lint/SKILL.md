---
name: wiki-lint
description: Run a read-only health check for staleness, drift, gaps, and unsupported claims. Use when the user says /wiki-lint, wiki lint, audit wiki, or check wiki health.
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
8. `.private-terms` (existence only, never its content), `.gitignore`,
   `git config core.hooksPath`, and the hooks folder
   `$(git rev-parse --git-path hooks)`;
9. file sizes from `wc -c`.

Do targeted source reads only where needed to verify claims.

## Step 3 - Checks

Find pages by Core map role (`index`, `log`, `log-archive`, `tracker`,
`decisions`, `risks`, `context`, `handoff`, `troubleshooting`, `glossary`) or
from the topic pages listed in SCHEMA `## Topics`.

Find checked sections by their `<!-- wiki:<id> -->` marker, or by the English
template heading in pages without markers. Flag a `context`, `handoff` or
`tracker` section found by neither, naming the marker to add.

### Core map

Flag roles pointing to missing files and broken relative links. A SCHEMA
without `## Core map` is a v1 wiki (old `overview.md`, `agent/`, `project/`
layout): check it against the v1 paths in the maintainer skill and suggest
`/wiki-init --adopt <root>`. A Core map row `activity (v1)` left by a v1 adopt
is part of the log until merged: suggest merging it.

### Staleness

For each page, read `git diff <source_commit>..HEAD -- <source>` for its listed
sources and judge the impact: flag the page when a change can affect what it
says (an interface, contract, command, config key or described behavior) and
name the affected claims; ignore cosmetic changes. Also flag:

- listed sources that are missing;
- confidence `low`;
- as signals to check, not verdicts: five or more commits touching listed
  sources since `source_commit`, or `updated` older than schema policy.

### Drift

Flag claims contradicted by code, tests, configs, CI, or current project docs.

### Orphans

Flag pages not linked from `index` or another useful page. Ignore `index`,
`SCHEMA.md`, `log`, `log-archive`, and an `activity (v1)` row.

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

Apply SCHEMA `## Evidence` by claim type. Flag verifications with no command,
no date or no code state (`@<short-sha>`), command output with no command,
descriptions with no precise source, decisions with no recorded approval,
risks with no stated assumption, and example output placed next to real
output. A `⚠️ NOT VERIFIED` without a reason is a finding too.

### Verified facts

Flag `Verified Facts` rows whose evidence sources changed after the
verification date (`git log --since=<date> -- <source>`) and are not marked
`⚠️ TO RE-VERIFY`; list the rows marked `⚠️ TO RE-VERIFY` as work to re-check.

### Single status

Flag status icons outside `tracker` (except pages that declare another
meaning at the top), IDs cited but missing from `tracker`, duplicated IDs,
and IDs reused for a different task.

Flag `tracker` rows without status, evidence, or next verification.

Flag Open rows without `Done when`, Done rows without `Criteria met` or
evidence, rows marked 🟢 whose criteria are not proven, Proposals with an ID or
a status icon, and external issue or PR state copied as status.

### Decisions

Flag decision files whose `status` is not `proposed`, `accepted`, `rejected`
or `superseded by NNNN`; `accepted` decisions without an `## Approval` naming
who, where and when; and reasons stated with no source (they should read
`Reasons not recorded.`).

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

A baton holding `No open work.` with no task rows is valid; flag it only when
the tracker has open rows.

### Budget

Measure with `wc -c`. Thresholds come from SCHEMA `## Budgets`; the
core read is the agent entry file (CLAUDE.md/AGENTS.md if present), `SCHEMA.md`, `index`, `context`, `handoff`, `tracker`, `risks`, `troubleshooting`, `glossary` and the last 10 `log` entries;
a closed phase is judged
from the project division in SCHEMA `## Project profile`. Flag any page over the single-page budget; the
core read over its budget (list each file's size); `log` over its
budget or holding entries of a closed phase. Suggest the split or the archive
cut.

### Confidentiality

Read `Sensitive data` from SCHEMA `## Project profile`. When it is `no`, skip
this section silently. When it is `yes`:

- run the maintainer skill's `scripts/check-private-terms.sh --all` and
  report its `file:line` and `file name:` output (never print the terms);
- flag a missing `.private-terms`;
- flag local-only paths that `git check-ignore -q` does not ignore;
- check the pre-commit hook. Let `H=$(git rev-parse --git-path hooks)`.
  If `git config core.hooksPath` is set, report "hook manager in use: verify
  the call line is configured" instead of installed or missing. Otherwise the
  hook is installed only when EITHER `$H/pre-commit` is the forbidden-terms
  script (`grep -q "private-terms" "$H/pre-commit"` and it contains the usage
  string `check-private-terms.sh [--staged|--all]`), OR
  `$H/check-private-terms.sh` exists AND
  `grep -q check-private-terms.sh "$H/pre-commit"` succeeds. Flag everything
  else (no hook, e.g. a fresh clone; an unrelated pre-commit without the call
  line; the script present but never called). Do not install it: print the
  exact commands in the report. With no pre-commit hook:
  `cp <maintainer skill>/scripts/check-private-terms.sh "$(git rev-parse --git-path hooks)/pre-commit"`
  and `chmod +x "$(git rev-parse --git-path hooks)/pre-commit"`. With an
  existing one: copy the script to
  `"$(git rev-parse --git-path hooks)/check-private-terms.sh"`, `chmod +x` it,
  and add `sh "$(git rev-parse --git-path hooks)/check-private-terms.sh" || exit 1`
  to the hook. `/wiki-init` offers the same as "install/repair the
  forbidden-terms hook only".

### Contradictions

Flag disagreements across topic pages, `decisions`, `risks`, `context`,
`tracker`, and source evidence.

Flag divergences between current behavior and a human requirement that
`risks` does not record (maintainer skill `## Conflicts`).

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
- Decisions: <n>
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
