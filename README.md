# Codebase Wiki LLM

Codebase Wiki LLM packages a cross-agent workflow for maintaining an
engineering-first software project wiki under `wiki/`.

The wiki is designed for real software work:

- engineers get architecture, module maps, invariants, safe-change guidance,
  verification commands, operations notes, and troubleshooting;
- project leads get status, roadmap, risks, requirements, milestones, and
  decisions;
- project documentation gets reusable, evidence-backed material under
  `project-docs/`;
- future agents get durable context, activity history, and handoff notes under
  `agent/`.

The same workflow is shipped for three hosts:

- **Codex** — exposed as the `codebase-wiki-llm` plugin (split skills).
- **Claude Code** — exposed as the `wiki-maintainer` plugin (slash commands + monolithic skill).
- **Antigravity** — exposed as an installable customization pack (rules + workflows + skill).

All variants share this single Git repository. Codex and Claude Code read their own marketplace manifests. Antigravity uses the install script to copy its customization pack into the expected Gemini/Antigravity folders.

The shared prompt content lives in [canonical](canonical). Host-specific plugin files under [plugins](plugins) are generated from those canonical sources and committed so marketplaces can consume the repo directly.

## What it creates

In a target repository, `/wiki-init` creates a local wiki shaped like this:

```text
wiki/
├── index.md
├── SCHEMA.md
├── log.md
├── overview.md
├── engineering/
│   ├── architecture.md
│   ├── data-model.md
│   ├── development.md
│   ├── testing.md
│   ├── operations.md
│   ├── troubleshooting.md
│   └── change-map.md
├── modules/
│   └── <module-or-area>.md
├── project/
│   ├── status.md
│   ├── roadmap.md
│   ├── milestones.md
│   ├── risks.md
│   ├── requirements.md
│   └── decisions.md
├── project-docs/
│   ├── project-brief.md
│   ├── value-proposition.md
│   ├── use-cases.md
│   ├── audience.md
│   ├── impact.md
│   ├── evidence.md
│   ├── demo-materials.md
│   └── faq.md
├── agent/
│   ├── context.md
│   ├── activity.md
│   └── handoff.md
└── glossary.md
```

Engineering pages are the source of technical truth. `project/` summarizes delivery state and decisions. `project-docs/` reuses supported claims for README, presentations, client docs, bids, proposals, and public project material. `agent/` keeps continuity between agent sessions.

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

## Canonical sources and generated packages

Edit shared wiki behavior only in `canonical/`:

```text
canonical/
├── maintainer.md
├── default-schema.md
├── rules/
│   └── wiki-context.md
└── workflows/
    ├── wiki-init.md
    ├── wiki-ingest.md
    ├── wiki-sync.md
    └── wiki-lint.md
```

Then regenerate the host packages:

```bash
scripts/generate-host-packages.py
scripts/check-generated.sh
```

The generator writes the host-specific files required by each environment:

- Codex skills under `plugins/codebase-wiki-llm/skills/`
- Claude Code commands and skill under `plugins/wiki-maintainer/`
- Antigravity rules, workflows, and skill under `plugins/antigravity-wiki-llm/.agent/`

Generated files include a `Generated from ...` marker and should not be edited directly. Commit both the canonical changes and the generated package updates before pushing.

Recommended release workflow:

```bash
# edit canonical/*
scripts/generate-host-packages.py
scripts/check-generated.sh
scripts/test-antigravity-pack.sh
git diff
git add .
git commit -m "Update wiki workflow prompts"
git push
```

After push, Codex and Claude Code marketplaces consume the updated generated
package files from this repository. Antigravity users should pull the repo and
rerun:

```bash
scripts/install-antigravity-wiki-llm.sh --yes
```

## Commands

Once installed, in any repository:

- `/wiki-init` — bootstrap an engineering-first project wiki.
- `/wiki-ingest [path]` — deep-dive into a file, directory, feature, or topic.
- `/wiki-sync` — surgically update existing wiki pages after small changes.
- `/wiki-lint` — read-only health report for staleness, drift, gaps, unsupported claims, and frontmatter issues.

## Mental model

- Marketplace location: this Git repository.
- Plugin location: `plugins/codebase-wiki-llm` (Codex), `plugins/wiki-maintainer` (Claude Code), or `plugins/antigravity-wiki-llm` (Antigravity).
- Canonical prompt location: `canonical/`.
- Generated package location: `plugins/`.
- Wiki location: per repository, always `<repo>/wiki/`.
- Schema location: per repository, `wiki/SCHEMA.md`.
- History location: per repository, `wiki/log.md`, `wiki/agent/activity.md`, and git history.

The plugin does not create a shared global wiki. It provides reusable skills,
commands, rules, and workflows that operate on the current repository's local
`wiki/` directory.

## Repository layout

```text
.agents/plugins/marketplace.json            <- Codex
.claude-plugin/marketplace.json             <- Claude Code
canonical/                                  <- shared prompt sources
scripts/generate-host-packages.py           <- generates host package files
scripts/check-generated.sh                  <- verifies generated files are current
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
