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

## Install in Codex

Clone the plugin from GitHub into your home-local plugins directory:

```bash
mkdir -p ~/plugins
git clone https://github.com/StefanoHernandez/codebase-wiki-llm.git ~/plugins/codebase-wiki-llm
```

Create or update the Codex marketplace file at `~/.agents/plugins/marketplace.json`.
If the file does not exist yet, use this full file:

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

If you already have a marketplace file, add only the object above to its
`plugins` array. Keep the `source.path` as `./plugins/codebase-wiki-llm`: with a
home-local marketplace, Codex resolves that path to `~/plugins/codebase-wiki-llm`.

Restart or refresh Codex plugin discovery after changing the marketplace file.

## Update

```bash
cd ~/plugins/codebase-wiki-llm
git pull
```

Restart or refresh Codex after updating if the plugin metadata changed.

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

## License

MIT. See [LICENSE](LICENSE).
