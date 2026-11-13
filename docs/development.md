# Developing the plugins

Notes for maintainers of this repository. Users only need the [README](../README.md).

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
│   ├── VERSION                  (release version for the plugin)
│   ├── maintainer.md
│   ├── default-schema.md
│   ├── partials/
│   ├── references/              (templates: context, handoff, decision, ...)
│   ├── rules/
│   │   └── wiki-context.md
│   ├── scripts/                 (resolve-wiki-root, remind-wiki-sync, check-private-terms)
│   └── workflows/
│       ├── wiki-init.md
│       ├── wiki-ingest.md
│       ├── wiki-sync.md
│       └── wiki-lint.md
└── secondbrain/
    ├── VERSION
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
python3 scripts/generate-host-packages.py   # wraps the two generators below
scripts/check-generated.sh
```

The generator writes the host-specific files required by each environment:

- Codex skills, hooks and scripts under `plugins/codebase-wiki-llm/`
- Claude Code commands, hooks, scripts and skills under `plugins/claude-codebase-wiki-llm/`
- Antigravity plugin under `plugins/antigravity-codebase-wiki-llm/` (`plugin.json`, `hooks.json`, `rules/`, `scripts/`, `skills/`)
- Codex SecondBrain skills under `plugins/secondbrain-wiki-llm/skills/`
- Claude Code SecondBrain commands and skills under `plugins/claude-secondbrain-wiki-llm/`
- Antigravity SecondBrain plugin under `plugins/antigravity-secondbrain-wiki-llm/`
- generic Agent Skills under `skills/`

Generated files include a `Generated from ...` marker and should not be edited directly. Commit both the canonical changes and the generated package updates before pushing.

## Maintaining this repo

- `canonical/` is the only source. Never edit generated files under `plugins/`
  or `skills/`.
- To release, edit `canonical/<plugin>/VERSION`, then run
  `python3 scripts/generate-host-packages.py`; it rewrites every manifest,
  including `.claude-plugin/marketplace.json`.
- A release changes `canonical/codebase/VERSION` and `VERSION` in
  `canonical/codebase/scripts/validate-wiki.py`. Change `FORMAT_VERSION` (and
  `format_version` in `default-schema.md`) only when the release adds an
  `upgrade:` check or changes a structure tools read.
- Run `scripts/install-dev-hooks.sh` once per clone to install the pre-commit
  drift guard (blocks commits when generated files are stale).
- Run `bash scripts/run-tests.sh` for the full test suite.

```bash
# edit canonical/...
python3 scripts/generate-host-packages.py
git add plugins skills .claude-plugin
bash scripts/run-tests.sh
git add . && git commit -m "Update wiki workflow prompts" && git push
```

After push, Codex and Claude Code marketplaces consume the updated generated
package files from this repository. Antigravity users who installed via
symlink see updates after `git pull`; users who copied the folder should rerun
the copy from the Install section.


## Repository layout

```text
.agents/plugins/marketplace.json            <- Codex
.claude-plugin/marketplace.json             <- Claude Code
canonical/                                  <- shared prompt sources and VERSION files by domain
scripts/generate-host-packages.py           <- wrapper: generates all host package files
scripts/generate-codebase-packages.py       <- generates Codebase Wiki packages
scripts/generate-secondbrain-packages.py    <- generates SecondBrain packages
scripts/check-generated.sh                  <- verifies generated files are current
scripts/run-tests.sh                        <- runs every test
scripts/install-dev-hooks.sh                <- installs this repo's pre-commit drift guard
scripts/validate-agent-handoff.py           <- validates agent context/handoff pages in a target wiki
canonical/codebase/scripts/validate-wiki.py <- installed read-only structural validator
scripts/test-wiki-validator.sh              <- behavioral fixtures and standalone package checks
scripts/test-agent-handoff-validator.sh      <- tests the validator against valid and invalid fixtures
scripts/test-*.sh                           <- tests: resolver, hooks, private terms, generators, validator
skills/                                     <- generated generic Agent Skills distribution
plugins/
├── codebase-wiki-llm/                      Codex variant
│   ├── .codex-plugin/plugin.json
│   ├── skills/                              (6 split skills)
│   ├── hooks/hooks.json                    (SessionStart resolver, UserPromptSubmit note)
│   ├── scripts/                            (resolve-wiki-root.sh, remind-wiki-sync.sh)
│   ├── assets/icon.svg
│   └── README.md
├── claude-codebase-wiki-llm/               Claude Code Codebase variant
│   ├── plugin.json
│   ├── commands/                           (/wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint)
│   ├── hooks/hooks.json                    (SessionStart resolver, UserPromptSubmit note)
│   ├── scripts/                            (resolve-wiki-root.sh, remind-wiki-sync.sh)
│   └── skills/
│       ├── wiki-maintainer/
│       └── wiki-context/
├── antigravity-codebase-wiki-llm/          Antigravity Codebase variant
│   ├── plugin.json
│   ├── hooks.json                          (PreInvocation note)
│   ├── scripts/                            (resolve-wiki-root.sh, remind-wiki-sync.sh)
│   ├── rules/AGENTS.md                     (always-on rule)
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
    ├── rules/AGENTS.md                     (always-on rule)
    └── skills/
        ├── secondbrain-maintainer/
        ├── secondbrain-init/
        ├── secondbrain-ingest/
        ├── secondbrain-sync/
        └── secondbrain-lint/
```


## Generic Agent Skills installers

The top-level `skills/` directory is generated from the same canonical prompts as the host
packages, for installers that expect a `skills/` folder, for example
`npx skills@latest add StefanoHernandez/codebase-wiki-llm`. This path is not yet a supported
install route: use the host-native installs in the README.

## Handoff validator (development CLI)

The development continuity CLI retains its narrower compatibility contract:

```bash
scripts/validate-agent-handoff.py path/to/repo/wiki
```

Without an argument it validates the folder named in `./.wikidir`, or `./wiki`.

It checks the minimum continuity contract: `agent/context.md`,
`agent/handoff.md`, frontmatter metadata, the `Baton For Next Coding Agent`
section, and at least one next task with start files, done criteria, and a
verification command.


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

