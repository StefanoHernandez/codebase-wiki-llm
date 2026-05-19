# Codebase Wiki LLM Plugin

Codex plugin for maintaining a living LLM wiki in the current repository.

This directory is the plugin package used by the root marketplace. Install the
marketplace from:

```text
https://github.com/StefanoHernandez/codebase-wiki-llm.git
```

Each project keeps its own `wiki/`; this plugin only provides the global Codex
skills that operate on the current project.

The skill files in this package are generated from the repository-level
`canonical/` sources. Edit those canonical files, then run
`scripts/generate-host-packages.py`.
