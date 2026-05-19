# Codebase Wiki LLM

Unified marketplace for the **wiki-maintainer** plugin — a living, LLM-owned wiki per codebase. Same idea, host-specific implementations:

- **Codex** — exposed as the `codebase-wiki-llm` plugin (split skills).
- **Claude Code** — exposed as the `wiki-maintainer` plugin (slash commands + monolithic skill).
- **Antigravity** — exposed as an installable customization pack (rules + workflows + skill).

All variants share this single Git repository. Codex and Claude Code read their own marketplace manifests. Antigravity uses the install script to copy its customization pack into the expected Gemini/Antigravity folders.

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

### On Antigravity

Clone this repository, then run:

```bash
scripts/install-antigravity-wiki-llm.sh
```

The installer copies the Antigravity pack from [plugins/antigravity-wiki-llm](plugins/antigravity-wiki-llm) into:

```text
~/.gemini/antigravity/
├── AGENTS.md
├── GEMINI.md
├── global_workflows/
├── rules/
└── skills/
```

It does not edit `~/.gemini/GEMINI.md` or `~/.gemini/AGENTS.md`, so Gemini CLI global rules are not modified.

## Why three plugin folders?

Codex, Claude Code, and Antigravity use different plugin formats:

| Aspect       | Codex                              | Claude Code                       | Antigravity                              |
| ------------ | ---------------------------------- | --------------------------------- | ---------------------------------------- |
| Discovery    | `.agents/plugins/marketplace.json` | `.claude-plugin/marketplace.json` | `scripts/install-antigravity-wiki-llm.sh` |
| Package path | `plugins/codebase-wiki-llm`        | `plugins/wiki-maintainer`         | `plugins/antigravity-wiki-llm`           |
| Manifest     | `.codex-plugin/plugin.json`        | `plugin.json`                     | `GEMINI.md`, `AGENTS.md`, `.agent/`      |
| Triggers     | Skills (one per operation)         | Slash commands + skill            | Workflows + rules + skill                |
| Package name | `codebase-wiki-llm`                | `wiki-maintainer`                 | `antigravity-wiki-llm`                   |

The host-specific paths do not collide, so a single repo serves all variants while keeping each host's expected format intact.

## Commands

Once installed, in any repository:

- `/wiki-init` — bootstrap `wiki/` in the current repository.
- `/wiki-ingest [path]` — deep-dive into a file, directory, or topic.
- `/wiki-sync` — small incremental update from recent source changes.
- `/wiki-lint` — read-only health report for drift, gaps, and staleness.

## Mental model

- Marketplace location: this Git repository.
- Plugin location: `plugins/codebase-wiki-llm` (Codex), `plugins/wiki-maintainer` (Claude Code), or `plugins/antigravity-wiki-llm` (Antigravity).
- Wiki location: per repository, always `<repo>/wiki/`.
- Schema location: per repository, `wiki/SCHEMA.md`.
- History location: per repository, `wiki/log.md` plus git history.

The plugin does not create a shared global wiki. It provides reusable skills/commands that operate on the current repository's local `wiki/` directory.

## Repository layout

```text
.agents/plugins/marketplace.json            <- Codex
.claude-plugin/marketplace.json             <- Claude Code
scripts/install-antigravity-wiki-llm.sh     <- Antigravity installer
plugins/
├── codebase-wiki-llm/                      Codex variant
│   ├── .codex-plugin/plugin.json
│   ├── skills/                              (6 split skills)
│   ├── assets/icon.svg
│   └── README.md
├── wiki-maintainer/                        Claude Code variant
│   ├── plugin.json
│   ├── commands/                           (/wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint)
│   └── skills/wiki-maintainer/
└── antigravity-wiki-llm/                   Antigravity variant
    ├── GEMINI.md
    ├── AGENTS.md
    └── .agent/
        ├── rules/
        ├── workflows/
        └── skills/codebase-wiki-maintainer/
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
