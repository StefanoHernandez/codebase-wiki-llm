# Codebase Wiki LLM

Global Codex plugin for maintaining a living LLM wiki per codebase.

The plugin is installed once, but each repository owns its own `wiki/`
directory. Running `/wiki-init` in a new project creates that project's wiki;
running `/wiki-sync`, `/wiki-ingest`, or `/wiki-lint` later updates or audits
that same local wiki.

## Mental model

- Plugin location: global, for example `~/plugins/codebase-wiki-llm`.
- Wiki location: per repository, always `<repo>/wiki/`.
- Schema location: per repository, `wiki/SCHEMA.md`.
- History location: per repository, `wiki/log.md` plus git history.

The plugin only provides Codex skills. It does not create a shared global wiki.

## Commands

Codex does not need separate executable slash-command files for this plugin.
When the user types one of these phrases, the corresponding skill handles it:

- `/wiki-init` - bootstrap `wiki/` in the current repository.
- `/wiki-ingest [path]` - deep-dive into a file, directory, or topic.
- `/wiki-sync` - small incremental update from recent source changes.
- `/wiki-lint` - read-only health report for drift, gaps, and staleness.

## Guardrail

Wiki operations may read source files but must not modify source files. They
write only under `wiki/`, except when the user explicitly asks for another
project change outside the wiki workflow.
