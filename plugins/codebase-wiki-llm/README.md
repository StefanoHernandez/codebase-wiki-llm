# Codebase Wiki LLM Plugin

Codex plugin for maintaining a living LLM wiki in the current repository.

This directory is the plugin package used by the root marketplace. Install the
marketplace from:

```text
https://github.com/StefanoHernandez/codebase-wiki-llm.git
```

Each project keeps its own wiki folder (`wiki/` by default, or the folder
named in `.wikidir`); this plugin only provides the global Codex
skills that operate on the current project. It also ships Codex hooks
(`hooks/hooks.json`): a `SessionStart` hook that resolves the wiki folder, asks
for one core read at a new context and flags a stale handoff, and a
`UserPromptSubmit` hook that adds a note at the next message (never a block)
when changed code is not covered by the wiki. Codex hook support is pending
verification in a real Codex session.

The skill files in this package are generated from the repository-level
`canonical/` sources. Edit those canonical files, then run
`scripts/generate-host-packages.py`.
