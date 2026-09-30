# /wiki-lint

Read-only health check for the repository-local wiki.

Requires the wiki maintainer skill. Respect `<wiki-root>/SCHEMA.md`.

## Step 0 - Resolve the wiki root

{{include:partials/resolve-wiki-root.md}}

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
6. root-level legacy docs listed by the schema.

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

Flag technical claims and `Verified Facts` rows with no date or no command,
and command output with no command. Flag example output placed next to real
output.

### Verified facts

Flag facts whose evidence sources changed after the verification date
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

Measure with `wc -c`. Flag any page over the single-page budget; the
per-session read set over its budget (list each file's size); `log` over its
budget or holding entries of a closed phase. Suggest the split or the archive
cut.

### Confidentiality

Only when `Sensitive data` is `yes`:

- run the maintainer skill's `scripts/check-private-terms.sh --all` and
  report its `file:line` output (never print the terms);
- flag a missing `.private-terms`;
- flag local-only paths that `git check-ignore -q` does not ignore;
- flag a missing pre-commit check: neither `.git/hooks/pre-commit` nor
  `.git/hooks/check-private-terms.sh` called from an existing pre-commit hook
  exists; suggest in the report that `/wiki-init` can install it (do not
  install it).

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

| Budget | File | Size | Limit |
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
