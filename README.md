# Codebase Wiki LLM

[![Latest release](https://img.shields.io/github/v/tag/StefanoHernandez/codebase-wiki-llm?label=release&sort=semver)](CHANGELOG.md)
[![MIT license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
![Hosts](https://img.shields.io/badge/hosts-Claude%20Code%20%7C%20Codex%20%7C%20Antigravity-lightgrey)

**A project wiki your coding agents keep, and you can trust.**

Codebase Wiki LLM is a plugin for Claude Code, Codex and Antigravity. It gives a repository a small,
evidence-backed Markdown wiki that agents read at the start of a session and update as they work:
one tracker as the only source of status, a log of what was done and how it was proven, one file
per decision, risks, and a handoff so the next session does not redo work.

> [!NOTE]
> Inspired by Andrej Karpathy's **LLM Wiki** idea: let LLM agents compile and maintain a linked
> Markdown knowledge base as the durable memory of a project, for people and agents alike.

This repository is a marketplace with two plugins:

- **Codebase Wiki LLM**: the engineering wiki for a software repository (this README).
- **SecondBrain Wiki LLM**: an adaptive personal and work knowledge vault ([below](#secondbrain-wiki-llm)).

The companion desktop app, [Codebase Wiki](https://github.com/StefanoHernandez/codebase-wiki-app),
shows the wiki to a person, records the approvals only a person can give and adds local code
search for agents. The plugin works without it.

## Why

- **Status lives in one place.** A tracker with stable IDs, done criteria and evidence; 🟢 only
  when the criteria are proven, ⚫ when a person closes a task without proof.
- **Claims carry evidence.** A verification names the command, its output and the code state
  (`@<sha>`); what cannot be proven is marked `⚠️ NOT VERIFIED`.
- **People keep the authority.** Decisions stay `proposed` until a person approves them; agents
  never close work on a person's behalf.
- **Sessions start fast.** `agent/context.md` and `agent/handoff.md` give a new agent the rules,
  the state and the next task.
- **The wiki is checked.** A deterministic validator (Python 3.10+, standard library only) checks
  structure, links, IDs and frontmatter; hooks remind the agent when changed code is not covered.

## Install

### Claude Code

```text
/plugin marketplace add https://github.com/StefanoHernandez/codebase-wiki-llm.git
/plugin install codebase-wiki-llm@stefano-wiki
```

Update with `/plugin marketplace update stefano-wiki`, then install again.

### Codex

Add a marketplace with the Git URL `https://github.com/StefanoHernandez/codebase-wiki-llm.git`,
then enable **Codebase Wiki LLM** in the Codex plugin UI.

### Antigravity

```bash
git clone https://github.com/StefanoHernandez/codebase-wiki-llm.git
cd codebase-wiki-llm
mkdir -p ~/.gemini/config/plugins
ln -s "$PWD/plugins/antigravity-codebase-wiki-llm" ~/.gemini/config/plugins/codebase-wiki-llm
```

With a symlink, `git pull` updates the plugin; use `cp -R` for a fixed copy. For one workspace
only, place the plugin under `.agents/plugins/codebase-wiki-llm/` at the workspace root.

<details>
<summary>Uninstall</summary>

- Claude Code: `/plugin uninstall codebase-wiki-llm@stefano-wiki`, optionally
  `/plugin marketplace remove stefano-wiki`.
- Codex: `codex plugin marketplace remove codebase-wiki-llm`.
- Antigravity: `rm ~/.gemini/config/plugins/codebase-wiki-llm` (`rm -rf` for a copy).

</details>

## Usage

In any repository:

| Command | What it does |
| --- | --- |
| `/wiki-init [folder] [--adopt <folder>]` | Creates the wiki, or adopts existing docs in place. |
| `/wiki-ingest [path]` | Deep-dives into a file, directory, feature or topic and writes it up. |
| `/wiki-sync` | Updates the pages a change touched: log entry, tracker, handoff. |
| `/wiki-lint` | Read-only health report: runs the validator, then checks drift, gaps and unsupported claims. |

In Codex and Antigravity the same operations are skills with the same names.

### `/wiki-init`

Init surveys the repository read-only, then asks **seven numbered questions in one message**, each
pre-filled: folder, wiki language, project division (phases, releases, sprints or none), topics,
sensitive data, agent entry file and parallel work. Reply `ok`, or override by number
(`3: releases, 5: yes`). Nothing is written before you confirm.

**Adopt mode.** If the repository already has documentation (or you run
`/wiki-init --adopt <folder>`), init maps your existing files in place, proposes only the missing
core pages and moves nothing without confirmation. Then it proposes a migration plan, one line per
move, each accepted or skipped. The same command upgrades an older wiki to the current format.

## What it creates

```text
<wiki-root>/
├── index.md             map and status table (cites IDs, never repeats status)
├── SCHEMA.md            configuration: profile, Core map, conventions, budgets, topics
├── log.md               recent log; log/ holds archives per phase or release
├── project/
│   ├── work-tracker.md  only source of status; stable IDs, never reused
│   ├── decisions/       one decision per file: 0001-<slug>.md
│   └── risks.md
├── agent/
│   ├── context.md       fast onboarding for a new agent or person
│   └── handoff.md       baton: state, next steps, what not to redo
├── troubleshooting.md   symptom, cause, fix, evidence
├── glossary.md
└── <topics>/            chosen at init: architecture/, environment/, operations/, …
```

Every path is a default: the **Core map** in `SCHEMA.md` maps each role to a file, so commands
never hard-code paths. Pages are written in the language you choose; stable
`<!-- wiki:… -->` markers keep the checks working in any language. Size budgets keep the core
cheap to read (page 20 KB, core read at a new context 60 KB, `log.md` 30 KB).

### Choosing the folder

| Folder | Use it for |
| --- | --- |
| `wiki/` (default) | Shared project documentation, committed like `docs/`. |
| `.wiki/` | Personal or agent working memory; stays out of git in repositories that ignore `.*`. |
| any name | `/wiki-init kb` writes `kb` into a one-line `.wikidir` file at the repository root. |

Obsidian ignores folders that start with `.`: open `.wiki/` itself as the vault. A gitignored wiki
has no history, and `git clean -xdf` deletes it. To move a wiki: `mv wiki .wiki`, then
`echo .wiki > .wikidir`.

## Validator

```bash
python3 <maintainer-skill>/scripts/validate-wiki.py path/to/repo/wiki
python3 <maintainer-skill>/scripts/validate-wiki.py --json path/to/repo/wiki
```

Shipped in every package; requires Python 3.10+ and nothing else. It is read-only. Exit `0` means
the documented structure passed, `1` lists `file:line` findings, `2` is an invocation or
configuration error. `upgrade:` lines say what an older wiki needs and never change the exit code.
It checks frontmatter, dates, sources, links, the Core map, tracker IDs and dependencies, markers,
the baton and 🟢/⚫ closures. It does not prove evidence or human authority: that stays with the
agent's review. Without Python, `/wiki-lint` says the check was skipped and never counts it as
passed.

## Hooks

| Hook | Claude Code | Codex | Antigravity | What it does |
| --- | :---: | :---: | :---: | --- |
| SessionStart | ✓ | ✓ | rule | Resolves the wiki folder, asks for one full core read at a new context, flags a handoff 5+ commits old. |
| UserPromptSubmit | ✓ | ✓ | — | At your next message, a note (never a block) when changed code is not covered by the wiki. |
| PreInvocation | — | — | ✓ | The same note, on the first model call of each turn. |
| git pre-commit | optional | optional | optional | With sensitive data on, blocks commits containing a term from `.private-terms` (reports the file, never the term). |

Codex and Antigravity hooks follow their documentation and have not yet been verified in a live
session. The note's state lives in `.git/codebase-wiki/` and is pruned after 30 days.

## SecondBrain Wiki LLM

An adaptive personal and work knowledge vault: a small core (`index.md`, `SCHEMA.md`, `log.md`,
`raw/`, `inbox/`, `archive/`) plus the domains you choose at init, such as `projects/`, `meetings/`,
`research/`, `tasks/`, `expenses/`, `people/` or `publications/`.

```text
/plugin install secondbrain-wiki-llm@stefano-wiki     # Claude Code
```

| Command | What it does |
| --- | --- |
| `/secondbrain-init` | Bootstraps a vault after surveying goals and existing material. |
| `/secondbrain-ingest [path-or-topic]` | Turns raw material, inbox notes, files or links into structured notes. |
| `/secondbrain-sync` | Updates existing notes after small changes. |
| `/secondbrain-lint` | Read-only report on structure, sources, sensitive data and stale pages. |

## Privacy and safety

The plugins are prompts, rules and local scripts: they send nothing anywhere. Wiki operations may
read source files but write only inside the wiki folder, plus what `/wiki-init` installs after you
confirm (`.wikidir`, a thin `CLAUDE.md`/`AGENTS.md`, `.gitattributes`, the optional pre-commit
hook). They never modify source code unless you ask for that outside the wiki workflow.

## Contributing

Shared behavior lives in [`canonical/`](canonical); the host packages under `plugins/` and `skills/`
are generated from it and committed. See [docs/development.md](docs/development.md) for the
layout, the generators and the release steps, and run `bash scripts/run-tests.sh` before a pull
request. Release history: [CHANGELOG.md](CHANGELOG.md).

Thanks to [Alessandro Cianfaglione](https://github.com/cianf4) for the configurable wiki folder
(`.wikidir`) and for using the wiki from its first versions. All contributors are listed in
[CONTRIBUTORS.md](CONTRIBUTORS.md).

## License

[MIT](LICENSE) © 2026 Stefano Hernandez
