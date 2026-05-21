# Stefano Wiki Plugins

This repository is a cross-agent marketplace for Markdown wiki workflows. It
ships two related plugins:

- **Codebase Wiki LLM** - an engineering-first software project wiki under
  `wiki/`.
- **SecondBrain Wiki LLM** - an adaptive personal and work knowledge vault for
  projects, documents, meetings, research, tasks, expenses, skills, people, and
  publications.

## Codebase Wiki LLM

Codebase Wiki LLM is designed for real software work:

- engineers get architecture, module maps, invariants, safe-change guidance,
  verification commands, operations notes, and troubleshooting;
- project leads get status, roadmap, risks, requirements, milestones, and
  decisions;
- project documentation gets reusable, evidence-backed material under
  `project-docs/`;
- future agents get durable context, activity history, and handoff notes under
  `agent/`.

> [!NOTE]
> **Inspiration & Credits**: This project is directly inspired by Andrej Karpathy's philosophy on LLM-managed knowledge bases (often referred to as the **LLM Wiki** pattern). By using LLM agents to compile, maintain, and link structured Markdown files as a durable knowledge layer, this workspace establishes long-term memory and execution safety for both human developers and AI copilots.

The Codebase Wiki workflow is shipped for three hosts:

- **Codex** — exposed as the `codebase-wiki-llm` plugin (split skills).
- **Claude Code** — exposed as the `codebase-wiki-llm` plugin (slash commands + skills).
- **Antigravity** — exposed as the `codebase-wiki-llm` plugin (rules + skills).

## SecondBrain Wiki LLM

SecondBrain Wiki LLM maintains a vault-local personal and work knowledge system.
It uses a small core plus adaptive domain folders selected during init:

```text
vault/
├── index.md
├── SCHEMA.md
├── log.md
├── raw/
├── inbox/
├── archive/
└── <active domains>/
```

Optional domains include `projects/`, `work/`, `personal/`, `meetings/`,
`research/`, `studies/`, `tasks/`, `expenses/`, `areas/`, `skills/`, `people/`,
and `publications/`.

It exposes four operations:

- `/secondbrain-init` - bootstrap an adaptive vault after surveying goals and
  existing material.
- `/secondbrain-ingest [path-or-topic]` - ingest raw material, inbox notes,
  files, folders, links, or topics into structured notes.
- `/secondbrain-sync` - surgically update existing vault notes after small
  changes.
- `/secondbrain-lint` - read-only health report for structure, sources,
  sensitive-data handling, stale pages, and operational gaps.

All variants share this single Git repository. Codex and Claude Code read their
own marketplace manifests. Antigravity auto-discovers plugin folders.

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

Codex discovers [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json)
and exposes both plugins:

- **Codebase Wiki LLM** from [plugins/codebase-wiki-llm](plugins/codebase-wiki-llm)
- **SecondBrain Wiki LLM** from [plugins/secondbrain-wiki-llm](plugins/secondbrain-wiki-llm)

Install or enable the plugin you want from the Codex plugin UI.

### On Claude Code

```text
/plugin marketplace add https://github.com/StefanoHernandez/codebase-wiki-llm.git
/plugin install codebase-wiki-llm@stefano-wiki
/plugin install secondbrain-wiki-llm@stefano-wiki
```

Claude Code discovers [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)
and exposes:

- **codebase-wiki-llm** from [plugins/claude-codebase-wiki-llm](plugins/claude-codebase-wiki-llm)
- **secondbrain-wiki-llm** from [plugins/claude-secondbrain-wiki-llm](plugins/claude-secondbrain-wiki-llm)

Update or remove later:

```text
/plugin marketplace update stefano-wiki
/plugin install codebase-wiki-llm@stefano-wiki
/plugin install secondbrain-wiki-llm@stefano-wiki
/plugin uninstall codebase-wiki-llm@stefano-wiki
/plugin uninstall secondbrain-wiki-llm@stefano-wiki
/plugin marketplace remove stefano-wiki
```

### On Antigravity

Antigravity auto-discovers plugins dropped into its plugins directory. Clone the
repo, then symlink (or copy) the plugin folder:

```bash
git clone https://github.com/StefanoHernandez/codebase-wiki-llm.git
cd codebase-wiki-llm
mkdir -p ~/.gemini/config/plugins
ln -s "$PWD/plugins/antigravity-codebase-wiki-llm" ~/.gemini/config/plugins/codebase-wiki-llm
ln -s "$PWD/plugins/antigravity-secondbrain-wiki-llm" ~/.gemini/config/plugins/secondbrain-wiki-llm
```

Use `cp -R` instead of `ln -s` if you do not want updates via `git pull`. Both
forms accept absolute paths; the `cd` above keeps `$PWD` unambiguous regardless
of where you cloned.

For workspace-scoped installs, place the plugin under
`.agents/plugins/codebase-wiki-llm/` at the workspace root instead.

Each Antigravity plugin contains a `plugin.json` marker, a `rules/` always-on
rule, and a `skills/` tree where maintainer knowledge and operations live as
auto-discovered skills.

## Uninstall

### From Codex

If you added this repository as a Codex marketplace, remove the marketplace:

```bash
codex plugin marketplace remove codebase-wiki-llm
```

If you used the manual local install below, also remove the local plugin copy
and the marketplace entry you added to `~/.agents/plugins/marketplace.json`.

### From Claude Code

Uninstall the plugin:

```text
/plugin uninstall codebase-wiki-llm@stefano-wiki
```

Optionally remove the marketplace too:

```text
/plugin marketplace remove stefano-wiki
```

### From Antigravity

Remove the plugin folder or symlink:

```bash
rm ~/.gemini/config/plugins/codebase-wiki-llm
rm ~/.gemini/config/plugins/secondbrain-wiki-llm
```

If you copied the folder rather than symlinking, use `rm -rf` against the same
path. For workspace-scoped installs remove `.agents/plugins/codebase-wiki-llm/`
under the workspace root instead.

## Why multiple plugin folders?

Codex, Claude Code, and Antigravity use different plugin formats. Each product
therefore has one package per host:

| Aspect       | Codex                              | Claude Code                         | Antigravity                            |
| ------------ | ---------------------------------- | ----------------------------------- | -------------------------------------- |
| Discovery    | `.agents/plugins/marketplace.json` | `.claude-plugin/marketplace.json`   | `~/.gemini/config/plugins/` auto-scan  |
| Codebase path | `plugins/codebase-wiki-llm`       | `plugins/claude-codebase-wiki-llm`  | `plugins/antigravity-codebase-wiki-llm` |
| SecondBrain path | `plugins/secondbrain-wiki-llm` | `plugins/claude-secondbrain-wiki-llm` | `plugins/antigravity-secondbrain-wiki-llm` |
| Manifest     | `.codex-plugin/plugin.json`        | `plugin.json`                       | `plugin.json` + `rules/` + `skills/`   |
| Triggers     | Skills (one per operation)         | Slash commands + skills             | Skills + always-on rule                |
| Package names | `codebase-wiki-llm`, `secondbrain-wiki-llm` | `codebase-wiki-llm`, `secondbrain-wiki-llm` | `codebase-wiki-llm`, `secondbrain-wiki-llm` |

The host-specific paths do not collide, so a single repo serves all variants
while keeping each host's expected format intact.

## Canonical sources and generated packages

Edit shared behavior only in the relevant canonical domain:

```text
canonical/
├── codebase/
│   ├── maintainer.md
│   ├── default-schema.md
│   ├── rules/
│   │   └── wiki-context.md
│   └── workflows/
│       ├── wiki-init.md
│       ├── wiki-ingest.md
│       ├── wiki-sync.md
│       └── wiki-lint.md
└── secondbrain/
    ├── maintainer.md
    ├── default-schema.md
    ├── rules/
    │   └── secondbrain-context.md
    └── workflows/
        ├── secondbrain-init.md
        ├── secondbrain-ingest.md
        ├── secondbrain-sync.md
        └── secondbrain-lint.md
```

Then regenerate the host packages:

```bash
scripts/generate-host-packages.py
scripts/generate-codebase-packages.py
scripts/generate-secondbrain-packages.py
scripts/check-generated.sh
```

The generator writes the host-specific files required by each environment:

- Codex skills under `plugins/codebase-wiki-llm/skills/`
- Claude Code commands and skills under `plugins/claude-codebase-wiki-llm/`
- Antigravity plugin under `plugins/antigravity-codebase-wiki-llm/` (`plugin.json`, `rules/`, `skills/`)
- Codex SecondBrain skills under `plugins/secondbrain-wiki-llm/skills/`
- Claude Code SecondBrain commands and skills under `plugins/claude-secondbrain-wiki-llm/`
- Antigravity SecondBrain plugin under `plugins/antigravity-secondbrain-wiki-llm/`

Generated files include a `Generated from ...` marker and should not be edited directly. Commit both the canonical changes and the generated package updates before pushing.

Recommended release workflow:

```bash
# edit canonical/codebase/* or canonical/secondbrain/*
scripts/generate-host-packages.py
scripts/check-generated.sh
git diff
git add .
git commit -m "Update wiki workflow prompts"
git push
```

After push, Codex and Claude Code marketplaces consume the updated generated
package files from this repository. Antigravity users who installed via
symlink see updates after `git pull`; users who copied the folder should rerun
the copy from the Install section.

## Commands

Once installed, in any repository:

- `/wiki-init` — bootstrap an engineering-first project wiki.
- `/wiki-ingest [path]` — deep-dive into a file, directory, feature, or topic.
- `/wiki-sync` — surgically update existing wiki pages after small changes.
- `/wiki-lint` — read-only health report for staleness, drift, gaps, unsupported claims, and frontmatter issues.
- `/secondbrain-init` — bootstrap an adaptive personal/work knowledge vault.
- `/secondbrain-ingest [path-or-topic]` — ingest raw material or inbox notes.
- `/secondbrain-sync` — surgically update existing vault notes.
- `/secondbrain-lint` — read-only health report for a SecondBrain vault.

## Mental model

- Marketplace location: this Git repository.
- Plugin location: `plugins/codebase-wiki-llm` (Codex), `plugins/claude-codebase-wiki-llm` (Claude Code), or `plugins/antigravity-codebase-wiki-llm` (Antigravity).
- SecondBrain plugin location: `plugins/secondbrain-wiki-llm` (Codex), `plugins/claude-secondbrain-wiki-llm` (Claude Code), or `plugins/antigravity-secondbrain-wiki-llm` (Antigravity).
- Canonical prompt location: `canonical/codebase/` and `canonical/secondbrain/`.
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
canonical/                                  <- shared prompt sources by domain
scripts/generate-host-packages.py           <- wrapper: generates all host package files
scripts/generate-codebase-packages.py       <- generates Codebase Wiki packages
scripts/generate-secondbrain-packages.py    <- generates SecondBrain packages
scripts/check-generated.sh                  <- verifies generated files are current
plugins/
├── codebase-wiki-llm/                      Codex variant
│   ├── .codex-plugin/plugin.json
│   ├── skills/                              (6 split skills)
│   ├── assets/icon.svg
│   └── README.md
├── claude-codebase-wiki-llm/               Claude Code Codebase variant
│   ├── plugin.json
│   ├── commands/                           (/wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint)
│   └── skills/
│       ├── wiki-maintainer/
│       └── wiki-context/
├── antigravity-codebase-wiki-llm/          Antigravity Codebase variant
│   ├── plugin.json
│   ├── rules/wiki.md                       (always-on rule)
│   └── skills/
│       ├── wiki-maintainer/                 (knowledge + default schema)
│       ├── wiki-init/
│       ├── wiki-ingest/
│       ├── wiki-sync/
│       └── wiki-lint/
├── secondbrain-wiki-llm/                   Codex SecondBrain variant
│   ├── .codex-plugin/plugin.json
│   └── skills/
│       ├── secondbrain-maintainer/
│       ├── secondbrain-context/
│       ├── secondbrain-init/
│       ├── secondbrain-ingest/
│       ├── secondbrain-sync/
│       └── secondbrain-lint/
├── claude-secondbrain-wiki-llm/            Claude Code SecondBrain variant
│   ├── plugin.json
│   ├── commands/                           (/secondbrain-init, /secondbrain-ingest, /secondbrain-sync, /secondbrain-lint)
│   └── skills/
│       ├── secondbrain-maintainer/
│       └── secondbrain-context/
└── antigravity-secondbrain-wiki-llm/        Antigravity SecondBrain variant
    ├── plugin.json
    ├── rules/secondbrain.md                (always-on rule)
    └── skills/
        ├── secondbrain-maintainer/
        ├── secondbrain-init/
        ├── secondbrain-ingest/
        ├── secondbrain-sync/
        └── secondbrain-lint/
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
