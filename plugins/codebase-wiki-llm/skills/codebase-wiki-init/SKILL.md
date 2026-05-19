---
name: codebase-wiki-init
description: Bootstrap a repository-local wiki/ using the global Codebase Wiki LLM plugin. Use when the user says /wiki-init, wiki init, bootstrap wiki, initialize codebase wiki, or asks to start a project wiki.
---

# Codebase Wiki Init

Handle `/wiki-init` for the current repository.

Load `codebase-wiki-maintainer` first and follow its rules.

## Preconditions

1. If `wiki/index.md` already exists, stop and ask whether to skip, run a focused ingest, or intentionally reinitialize.
2. If the current directory does not look like a code repository, ask for confirmation.

## Survey

Read enough to form a map:
- Top-level files and directories.
- `README.md` or equivalent.
- Architecture-shaping docs.
- Package or project manifests.
- Main source directories.
- Test directories.

Do not read every source file during the first survey.

## Confirm plan

Before writing, report:
- One-sentence project summary.
- Proposed wiki structure.
- Proposed module pages.
- Root docs that might later be superseded.

Ask the user to confirm or adjust scope.

## Create wiki

After confirmation:

1. Create `wiki/`.
2. Copy the plugin default schema from `codebase-wiki-maintainer/default-schema.md` to `wiki/SCHEMA.md`.
3. Fill in repo-specific scope notes in `wiki/SCHEMA.md` when known.
4. Create:
   - `wiki/index.md`
   - `wiki/log.md`
   - `wiki/overview.md`
   - `wiki/architecture/decisions.md`
   - `wiki/architecture/data-model.md`
   - `wiki/glossary.md`
   - `wiki/modules/`
5. Write initial module pages for the high-confidence areas identified in the survey.
6. Add frontmatter to every page.
7. Append the init entry to `wiki/log.md`.

## Report

Finish with:
- Pages created.
- Any docs proposed for later retirement.
- Suggested next step, usually `/wiki-lint`.

Do not modify source files during init.
