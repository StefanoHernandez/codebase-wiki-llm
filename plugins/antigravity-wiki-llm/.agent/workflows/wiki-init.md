# /wiki-init

Bootstrap a living wiki for the current repository.

## Preconditions

1. If `wiki/index.md` already exists, stop and ask whether to skip, run
   `/wiki-ingest`, or intentionally reinitialize.
2. If the current directory does not look like a code repository, ask for
   confirmation before writing.

## Survey

Read enough to map the repository:

- Top-level files and directories.
- README or equivalent project docs.
- Architecture-shaping docs.
- Package manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, or
  similar.
- Main source and test directories.

Do not read every source file during the first survey.

## Confirm

Before writing, tell the user:

- One-sentence project summary.
- Proposed wiki structure.
- Proposed module pages.
- Root docs that might later be superseded.

Ask for confirmation.

## Create

After confirmation:

1. Create `wiki/`.
2. Copy `default-schema.md` from the `codebase-wiki-maintainer` skill to
   `wiki/SCHEMA.md`.
3. Create `wiki/index.md`, `wiki/log.md`, `wiki/overview.md`,
   `wiki/architecture/decisions.md`, `wiki/architecture/data-model.md`,
   `wiki/glossary.md`, and `wiki/modules/`.
4. Add frontmatter to every page.
5. Write concise, verified initial content.
6. Append the init entry to `wiki/log.md`.

Never modify source files during init.
