# Codebase Wiki LLM

Codex marketplace for maintaining a living LLM wiki per codebase.

The marketplace contains the `codebase-wiki-llm` plugin. The plugin is installed
once in Codex, but each repository owns its own `wiki/` directory. Running
`/wiki-init` in a project creates that project's wiki; running `/wiki-sync`,
`/wiki-ingest`, or `/wiki-lint` later updates or audits that same local wiki.

## Install in Codex from GitHub

In Codex, add a new marketplace and use this Git URL:

```text
https://github.com/StefanoHernandez/codebase-wiki-llm.git
```

Codex reads this repository's marketplace file:

```text
.agents/plugins/marketplace.json
```

That marketplace exposes the plugin at:

```text
plugins/codebase-wiki-llm
```

After adding the marketplace, install or enable **Codebase Wiki LLM** from the
Codex plugin UI.

## Manual local install

If you prefer a manual home-local install:

```bash
mkdir -p ~/plugins
git clone https://github.com/StefanoHernandez/codebase-wiki-llm.git /tmp/codebase-wiki-llm
cp -R /tmp/codebase-wiki-llm/plugins/codebase-wiki-llm ~/plugins/codebase-wiki-llm
```

Then create or update `~/.agents/plugins/marketplace.json` with:

```json
{
  "name": "stefano-local",
  "interface": {
    "displayName": "Stefano Local Plugins"
  },
  "plugins": [
    {
      "name": "codebase-wiki-llm",
      "source": {
        "source": "local",
        "path": "./plugins/codebase-wiki-llm"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Restart or refresh Codex plugin discovery after changing marketplaces.

## Mental model

- Marketplace location: this Git repository.
- Plugin location inside the marketplace: `plugins/codebase-wiki-llm`.
- Wiki location: per repository, always `<repo>/wiki/`.
- Schema location: per repository, `wiki/SCHEMA.md`.
- History location: per repository, `wiki/log.md` plus git history.

The plugin does not create a shared global wiki. It provides reusable Codex
skills that operate on the current repository's local `wiki/` directory.

## Commands

Codex does not need separate executable slash-command files for this plugin.
When the user types one of these phrases, the corresponding skill handles it:

- `/wiki-init` - bootstrap `wiki/` in the current repository.
- `/wiki-ingest [path]` - deep-dive into a file, directory, or topic.
- `/wiki-sync` - small incremental update from recent source changes.
- `/wiki-lint` - read-only health report for drift, gaps, and staleness.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/codebase-wiki-llm/.codex-plugin/plugin.json
plugins/codebase-wiki-llm/skills/
plugins/codebase-wiki-llm/assets/
```

## Guardrail

Wiki operations may read source files but must not modify source files. They
write only under `wiki/`, except when the user explicitly asks for another
project change outside the wiki workflow.

## License

MIT. See [LICENSE](LICENSE).
