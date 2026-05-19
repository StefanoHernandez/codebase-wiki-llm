# Codebase Wiki LLM

Unified marketplace for the **wiki-maintainer** plugin — a living, LLM-owned wiki per codebase. Same idea, two host-specific implementations:

- **Codex** — exposed as the `codebase-wiki-llm` plugin (split skills).
- **Claude Code** — exposed as the `wiki-maintainer` plugin (slash commands + monolithic skill).

Both share this single Git repository. Each host reads its own marketplace manifest and picks the plugin folder that fits its format.

## Install

### On Codex

In Codex, add a new marketplace with this Git URL:

```text
https://github.com/StefanoHernandez/codebase-wiki-llm.git
```

Codex discovers [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) and exposes the **Codebase Wiki LLM** plugin from [plugins/codebase-wiki-llm](plugins/codebase-wiki-llm). Install or enable it from the Codex plugin UI.

### On Claude Code

```text
/plugin marketplace add https://github.com/StefanoHernandez/codebase-wiki-llm.git
/plugin install wiki-maintainer@stefano-wiki
```

Claude Code discovers [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and installs the **wiki-maintainer** plugin from [plugins/wiki-maintainer](plugins/wiki-maintainer).

Update or remove later:

```text
/plugin marketplace update stefano-wiki
/plugin install wiki-maintainer@stefano-wiki
/plugin uninstall wiki-maintainer@stefano-wiki
/plugin marketplace remove stefano-wiki
```

## Why two plugin folders?

Codex and Claude Code use different plugin formats:

| Aspect            | Codex                                          | Claude Code                        |
| ----------------- | ---------------------------------------------- | ---------------------------------- |
| Marketplace file  | `.agents/plugins/marketplace.json`             | `.claude-plugin/marketplace.json`  |
| Plugin manifest   | `plugins/<name>/.codex-plugin/plugin.json`     | `plugins/<name>/plugin.json`       |
| Triggers          | Skills (one per operation)                     | Slash commands + skill             |
| Plugin name       | `codebase-wiki-llm`                            | `wiki-maintainer`                  |

The two manifest paths do not collide, so a single repo serves both marketplaces. Each host only sees its own folder.

## Commands

Once installed, in any repository:

- `/wiki-init` — bootstrap `wiki/` in the current repository.
- `/wiki-ingest [path]` — deep-dive into a file, directory, or topic.
- `/wiki-sync` — small incremental update from recent source changes.
- `/wiki-lint` — read-only health report for drift, gaps, and staleness.

## Mental model

- Marketplace location: this Git repository.
- Plugin location: `plugins/codebase-wiki-llm` (Codex) or `plugins/wiki-maintainer` (Claude Code).
- Wiki location: per repository, always `<repo>/wiki/`.
- Schema location: per repository, `wiki/SCHEMA.md`.
- History location: per repository, `wiki/log.md` plus git history.

The plugin does not create a shared global wiki. It provides reusable skills/commands that operate on the current repository's local `wiki/` directory.

## Repository layout

```text
.agents/plugins/marketplace.json            ← Codex
.claude-plugin/marketplace.json             ← Claude Code
plugins/
├── codebase-wiki-llm/                      Codex variant
│   ├── .codex-plugin/plugin.json
│   ├── skills/                              (6 split skills)
│   ├── assets/icon.svg
│   └── README.md
└── wiki-maintainer/                        Claude Code variant
    ├── plugin.json
    ├── commands/                           (/wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint)
    └── skills/wiki-maintainer/
```

## Manual local install (Codex)

If you prefer a manual home-local install:

```bash
mkdir -p ~/plugins
git clone https://github.com/StefanoHernandez/codebase-wiki-llm.git /tmp/codebase-wiki-llm
cp -R /tmp/codebase-wiki-llm/plugins/codebase-wiki-llm ~/plugins/codebase-wiki-llm
```

Then create or update `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "stefano-local",
  "interface": { "displayName": "Stefano Local Plugins" },
  "plugins": [
    {
      "name": "codebase-wiki-llm",
      "source": { "source": "local", "path": "./plugins/codebase-wiki-llm" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

Restart or refresh Codex plugin discovery after changing marketplaces.

## Guardrail

Wiki operations may read source files but must not modify source files. They write only under `wiki/`, except when the user explicitly asks for another project change outside the wiki workflow.

## License

MIT. See [LICENSE](LICENSE).
