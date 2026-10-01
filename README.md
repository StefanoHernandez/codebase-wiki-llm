# Stefano Wiki Plugins

This repository is a cross-agent marketplace for Markdown wiki workflows. It
ships two related plugins:

- **Codebase Wiki LLM** - an engineering-first software project wiki under
  `wiki/` by default, or a folder you choose such as `.wiki/`.
- **SecondBrain Wiki LLM** - an adaptive personal and work knowledge vault for
  projects, documents, meetings, research, tasks, expenses, skills, people, and
  publications.

## Codebase Wiki LLM

Codebase Wiki LLM is designed for real software work. It keeps a small,
evidence-backed wiki that a person or a coding agent can trust:

- one work tracker as the only source of status, with stable IDs;
- one log, decisions as one file each, risks, troubleshooting, glossary;
- `agent/context.md` and `agent/handoff.md` so a new session starts fast and
  does not redo work;
- optional topics chosen at init (architecture, environment, operations, ...).

> [!NOTE]
> **Inspiration & Credits**: This project is directly inspired by Andrej Karpathy's philosophy on LLM-managed knowledge bases (often referred to as the **LLM Wiki** pattern). By using LLM agents to compile, maintain, and link structured Markdown files as a durable knowledge layer, this workspace establishes long-term memory and execution safety for both human developers and AI copilots.

The Codebase Wiki workflow is shipped for three hosts:

- **Codex** — exposed as the `codebase-wiki-llm` plugin (split skills).
- **Claude Code** — exposed as the `codebase-wiki-llm` plugin (slash commands + skills).
- **Antigravity** — exposed as the `codebase-wiki-llm` plugin (rules + skills).

### Changes in 0.9.1

- Reminder coverage tracks source content: another edit at a covered path or
  a path already dirty at session start prompts another next-turn note.
- Every maintainer distribution ships a standalone deterministic wiki
  validator. `/wiki-lint` runs it before the agent's semantic review.
- Tracker terminal rows distinguish 🟢 verified completion from ⚫ work a
  person explicitly closed without proven criteria. Handoff cites tracker IDs.
- Already approved decisions can be recorded as `accepted` with who, where
  and when; new unresolved ideas remain `proposed`.
- Automated checks precede the main/tag push. Real-host Codex, Claude Code
  and Antigravity trials remain pending until Stefano's trials after the push:
  [release checklist](docs/release-checklist.md).

### Changes in 0.9.0

- v2 core: a small fixed core (index, log, tracker, decisions, risks, context,
  handoff, troubleshooting, glossary) located through the `SCHEMA.md` Core map.
- One log: `agent/activity.md` is merged into `log.md`.
- The project-docs, engineering and overview pages and the export are no longer
  built in; add them as topics when you need them.
- Hooks: SessionStart resolves the wiki root, asks for one full core read at a
  new context and flags a stale handoff; a note at your next message (never a
  block) says when changed code is not covered by the wiki.
- Evidence proportional to the claim, with the code state (`@<sha>`,
  `+local`); a fact that can no longer be proven is marked `⚠️ TO RE-VERIFY`.
- Tracker with goal, done criteria and a separate Proposals list; 🟢 only with
  proven criteria. Decisions stay `proposed` until a person approves them.
- Pages in the language you choose; stable `<!-- wiki:… -->` markers keep the
  checks working.
- Adopt maps existing docs in place, then proposes a migration plan as one
  numbered list, each move accepted or skipped; `/wiki-sync` archives the log
  by rule.
- Release gate: [docs/release-checklist.md](docs/release-checklist.md).
- v1 wikis keep working; run `/wiki-init --adopt <folder>` to move to v2.

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

In a target repository, `/wiki-init` creates a local wiki shaped like this
(every path is a default; the Core map in `SCHEMA.md` is the source of truth):

```text
<wiki-root>/
├── index.md             map + status table (cites IDs, never repeats status)
├── SCHEMA.md            configuration for the agent
├── log.md               recent log
├── log/                 log archives, one per closed phase/release/sprint/quarter
├── project/
│   ├── work-tracker.md  only source of status; stable IDs, never reused
│   ├── decisions/       one decision per file: 0001-<slug>.md
│   └── risks.md
├── agent/
│   ├── context.md       fast onboarding for a new agent or person
│   └── handoff.md       baton: state, next steps, what not to redo
├── troubleshooting.md   symptom, cause, fix, evidence
├── glossary.md          terms, acronyms, internal names
└── <topics>/            chosen at init, e.g. architecture/, environment/, operations/
```

`SCHEMA.md` holds the project profile, the **Core map** (role to path, so
commands never hard-code paths), conventions (ID prefix `T`; 🟢 done and
verified, ⚫ closed by a person without proven criteria, 🟡 in progress,
⚪ to do, 🔴 blocked), size budgets (page 20 KB,
core read at a new context 60 KB, `log.md` 30 KB) and the topics table. Edit
these files yourself or ask the agent; it records changes in `SCHEMA.md`.

Evidence is proportional to the claim: a verification gives the command, its
essential output and the code state; a description names the source file. What
cannot be proven is marked `⚠️ NOT VERIFIED` (or `⚠️ TO RE-VERIFY` when it
can no longer be proven). Each log entry names its author (`human` or `agent`).

### `/wiki-init`: survey, then one message

Init first surveys the repo read-only (existing docs, `CLAUDE.md`/`AGENTS.md`,
README language, project type, `.gitignore`). It then asks **seven numbered
questions in one message**, each pre-filled. Reply `ok`, or override by number
(`3: releases, 5: yes`):

1. Folder: adopt existing docs, or a new `wiki` / `.wiki`.
2. Wiki language.
3. Project division: phases/WP, releases, sprints/milestones, or none.
4. Topics (pre-checked from the survey).
5. Sensitive data: no, or yes (forbidden terms, local-only paths, git
   pre-commit check).
6. Agent entry file: a thin `CLAUDE.md`/`AGENTS.md` pointing to
   `agent/context.md`. An existing file is never overwritten.
7. Parallel work: `merge=union` for the log in `.gitattributes`, so entries
   written in parallel merge without conflicts.

Nothing is written before you confirm.

### Adopt mode

If the survey finds an existing docs folder (or you run
`/wiki-init --adopt <folder>`), init writes `.wikidir` and `SCHEMA.md`,
inserts section markers in the adopted core pages, and moves files only for
the migration moves you accept (plus `.gitattributes` if you chose item 7).
The Core map points at your existing files, only missing core roles are
proposed, and nothing is moved or renamed without confirmation. Once the map
works in place, init proposes a migration plan toward the default layout, one
line per move that you accept or skip; skipped moves stay mapped where they
are. A v1 wiki (has `SCHEMA.md`, no Core map) is handled the same way; until
then sync and lint keep working on it with the v1 paths listed in the
maintainer skill and suggest running adopt. After adopt, `agent/activity.md` stays mapped as
`activity (v1)` and counts as part of the log until you merge it.

## Choosing the wiki folder

`/wiki-init` creates the wiki in `wiki/` unless you choose another folder:

```text
/wiki-init            # proposes wiki/, or .wiki/ when git already ignores it
/wiki-init .wiki      # hidden; local-only in repos that ignore .* paths
/wiki-init kb         # any single folder name
```

Pick by audience:

- `wiki/` - shared project documentation, committed like `docs/`.
- `.wiki/` - personal or agent working memory. In company repositories whose
  `.gitignore` ignores every `.*` path, it stays out of shared git history.

When the folder is not `wiki/`, init writes a one-line pointer at the
repository root so every later session finds it. Like `.nvmrc` or
`.python-version`, it contains only the value:

```text
.wikidir    ->    .wiki
```

Every workflow resolves the folder the same way: `.wikidir` first, then
an existing `wiki/SCHEMA.md`. Claude Code and Codex also resolve it at session start
with a plugin `SessionStart` hook; Antigravity's always-on rule does the same. Existing `wiki/` wikis keep working unchanged.

Notes:

- Obsidian ignores folders that start with `.`. Open `.wiki/` itself as the
  vault instead of the whole repository.
- A gitignored wiki has no git history, and `git clean -xdf` deletes it.
- To move an existing wiki: `mv wiki .wiki`, then `echo .wiki > .wikidir`
  (bash and PowerShell both work: UTF-8, UTF-8 with BOM, and UTF-16 are read).

## Hooks

| Hook | Claude Code | Codex | Antigravity | What it does |
| ---- | :---------: | :---: | :---------: | ------------ |
| SessionStart | yes | yes (per Codex docs; not yet verified in a live session) | no (its always-on rule resolves the root and asks for the core read; no stale-handoff note) | Resolves the wiki folder, prints a `wiki_root` line and a `new context` line asking the agent to read the core once, and notes a stale handoff (5 or more commits since it was updated). |
| UserPromptSubmit | yes | yes (per Codex docs; not yet verified in a live session) | — | At your next message, adds a note (never a block) when code changed in this session and the wiki does not cover it. |
| PreInvocation | — | — | yes (checked against Antigravity docs, not yet in a live session) | The same note, on the first model call of each turn. |
| git pre-commit | optional | optional | optional | Blocks commits whose contents or file names contain a term from `<wiki-root>/.private-terms` (reports `file:line` or the file name, never the term; binary files are skipped). |

Claude Code and Codex share one `hooks/hooks.json`. Antigravity's `hooks.json`
has the PreInvocation note only; its always-on rule resolves the wiki root and
asks for the core read instead of a SessionStart hook.

The note looks at code changed since the session's first message (commits
and uncommitted files; files already dirty then are left out) and at wiki
files edited since (by modification time, so a wiki git ignores works too).
It speaks when no wiki file changed, or when a page whose `sources:` list a
changed file was not updated, once per changed set of files; once the wiki
covers a change, only later changes count. Changes inside a submodule show as
the submodule path. Its state lives in `.git/codebase-wiki/` and is pruned
after 30 days.

The forbidden-terms pre-commit check is not a plugin hook: `/wiki-init`
installs it in the repo's hooks folder (`git rev-parse --git-path hooks`) when
sensitive data is on, or shows the call line when `core.hooksPath` points to a
hook manager. Codex runs the note with `--host claude` because it receives the
same payload shape.

## Install

### One-command installer target

This repository keeps two install surfaces committed:

- `plugins/` for host-native plugin marketplaces and Antigravity plugin
  discovery;
- `skills/` for generic Agent Skills installers that expect a top-level skills
  directory.

The desired cross-agent install model is:

```bash
npx skills@latest add StefanoHernandez/codebase-wiki-llm
```

That command style is compatible with the public `skills` CLI ecosystem used by
multi-agent skill repositories. The top-level `skills/` directory is generated
from the same canonical prompts as the host-native plugins, so generic agents
can install the shared skills while Codex, Claude Code, Antigravity, OpenCode,
Cursor, and similar tools can still use host-specific packaging when available.

Until that installer layer is finalized, use the host-native install paths
below.

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

## Commands

Once installed, in any repository:

- `/wiki-init [folder]` — bootstrap an engineering-first project wiki (default folder `wiki/`).
- `/wiki-ingest [path]` — deep-dive into a file, directory, feature, or topic.
- `/wiki-sync` — surgically update existing wiki pages after small changes.
- `/wiki-lint` — read-only health report for staleness, drift, gaps, unsupported claims, and frontmatter issues.
- `/secondbrain-init` — bootstrap an adaptive personal/work knowledge vault.
- `/secondbrain-ingest [path-or-topic]` — ingest raw material or inbox notes.
- `/secondbrain-sync` — surgically update existing vault notes.
- `/secondbrain-lint` — read-only health report for a SecondBrain vault.

Installed structural validator for project wikis (Codebase 0.9.1):

```bash
python3 <maintainer-skill>/scripts/validate-wiki.py path/to/repo/wiki
```

The same standalone script is shipped in the Codex, Claude Code and
Antigravity maintainer skills and `skills/codebase-wiki-llm`. It requires
**Python 3.10+**, standard library only. This is an optional `/wiki-lint`
dependency: if Python is missing or older, the agent explicitly reports that
deterministic validation was skipped and continues its read-only review.
It never installs a runtime implicitly or treats a skipped check as passing.
The main hooks still require only POSIX shell and Git.

The script is read-only. Exit 0 means documented structure passed, 1 means
file/line findings, and 2 means invocation/configuration error. Sources are
relative to the target repository (nearest ancestor with `.git`, or the wiki's
parent without Git); links are relative to each page. It checks the documented
scalar frontmatter and indented source lists, real ISO dates, confidence,
sources, inline/reference Markdown file links, Core map roles and paths,
tracker IDs, continuity markers (with legacy English heading fallback), baton
rows and explicit green/black closure claims. Fenced code and external links
are ignored. It does not parse arbitrary YAML or every Markdown extension,
read `.private-terms`, execute commands, or prove evidence and human authority.
Semantic checks still belong to the agent.

The development continuity CLI retains its narrower compatibility contract:

```bash
scripts/validate-agent-handoff.py path/to/repo/wiki
```

Without an argument it validates the folder named in `./.wikidir`, or `./wiki`.

It checks the minimum continuity contract: `agent/context.md`,
`agent/handoff.md`, frontmatter metadata, the `Baton For Next Coding Agent`
section, and at least one next task with start files, done criteria, and a
verification command.

## Mental model

- Marketplace location: this Git repository.
- Plugin location: `plugins/codebase-wiki-llm` (Codex), `plugins/claude-codebase-wiki-llm` (Claude Code), or `plugins/antigravity-codebase-wiki-llm` (Antigravity).
- SecondBrain plugin location: `plugins/secondbrain-wiki-llm` (Codex), `plugins/claude-secondbrain-wiki-llm` (Claude Code), or `plugins/antigravity-secondbrain-wiki-llm` (Antigravity).
- Canonical prompt location: `canonical/codebase/` and `canonical/secondbrain/`.
- Generated package location: `plugins/`.
- Wiki location: per repository, `<repo>/wiki/` by default, or the folder named in `<repo>/.wikidir`.
- Schema location: per repository, `<wiki folder>/SCHEMA.md`.
- History location: per repository, `<wiki folder>/log.md` (plus `log/` archives) and git history when the wiki is tracked.

The plugin does not create a shared global wiki. It provides reusable skills,
commands, rules, and workflows that operate on the current repository's local
wiki folder.

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

Wiki operations may read source files but must not modify source files. They
write only under the wiki folder (plus `.wikidir` when `/wiki-init` picks a
folder other than `wiki/`, and an optional git pre-commit hook and thin agent
entry file that init installs after you confirm), except when the user
explicitly asks for another project change outside the wiki workflow.

## License

MIT. See [LICENSE](LICENSE).
