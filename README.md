# claude-wiki-plugin

A Claude Code plugin that keeps a **living, LLM-owned wiki** of your codebase under `wiki/`. The agent reads it before answering questions, updates it after changes, and flags drift.

Inspired by the "LLM Wiki" pattern (Karpathy, 2026), adapted for source code that mutates.

---

## What you get

Four slash commands and one skill that work together:

| Command | What it does |
|---|---|
| `/wiki-init` | Bootstrap `wiki/` in a new repo. Surveys the project, proposes a structure, asks for confirmation, then writes the initial pages. |
| `/wiki-ingest [path]` | Deliberate deep-dive into a file/directory/topic. Updates affected wiki pages, the index, and the log. |
| `/wiki-sync` | Fast incremental update from recent diffs/modified files. Run after a task that touched source code. |
| `/wiki-lint` | Health check — reports staleness, drift, orphans, gaps, contradictions. Never silently edits. |

The `wiki-maintainer` skill defines the conventions: page frontmatter, confidence levels, decay policy, log/index discipline.

---

## Installation

In Claude Code:

```
/plugin marketplace add StefanoHernandez/claude-wiki-plugin
/plugin install wiki-maintainer@stefano-wiki
```

That's it. The four `/wiki-*` commands are now available and the skill loads automatically when you work under `wiki/`.

### Update

```
/plugin marketplace update stefano-wiki
/plugin install wiki-maintainer@stefano-wiki
```

### Uninstall

```
/plugin uninstall wiki-maintainer@stefano-wiki
/plugin marketplace remove stefano-wiki
```

---

## Typical workflow

1. **First time in a repo** — run `/wiki-init`. Confirm the scope, let it write the initial pages.
2. **After a substantive change** — run `/wiki-ingest <path>` for a deliberate update of the affected area.
3. **After any task that touched code** — run `/wiki-sync` for a quick incremental refresh.
4. **Periodically** — run `/wiki-lint` to surface stale pages, contradictions, gaps.

The wiki is written for two readers: a human browsing, and a future agent session loading context. Both should find it useful.

---

## Wiki layout (default)

```
wiki/
├── SCHEMA.md           # repo-specific conventions (read first)
├── index.md            # catalog of every page
├── log.md              # append-only timeline of ingests/syncs/lints
├── overview.md         # one-page orientation
├── architecture/
│   ├── decisions.md    # ADRs
│   └── data-model.md
├── modules/            # one page per major area
└── glossary.md
```

`SCHEMA.md` is the per-repo constitution. It can override layout, scope, decay policy, style. The skill respects it over its defaults.

---

## Page conventions

Every wiki page has YAML frontmatter:

```yaml
---
title: Short descriptive title
updated: 2026-04-14
sources:
  - src/routes/nodes.ts
  - src/middleware/auth.ts
source_commit: abc123        # optional, if git available
confidence: high             # high | medium | low
---
```

- **Confidence decays** as source files change after `source_commit`. Lint flags low-confidence pages.
- **Supersession over deletion**: when a claim is wrong, write the corrected version and note what it replaced. The wiki keeps a visible history of its own understanding.
- **Cross-references** use standard relative markdown links (not `[[wikilinks]]`).

Full conventions in [`plugins/wiki-maintainer/skills/wiki-maintainer/SKILL.md`](plugins/wiki-maintainer/skills/wiki-maintainer/SKILL.md).

---

## Design principles

- **Do not invent.** If a claim can't be verified from code or docs, it doesn't go in.
- **Cite sources** in frontmatter — the page declares which files it describes.
- **Propose, don't delete.** Lint surfaces problems; the human decides what to remove.
- **Never modify source code** during wiki operations.
- **One page, one concept.** Split when a page exceeds ~200 lines.

---

## Requirements

- Claude Code with plugin marketplace support.
- Works with or without git. Without git, `source_commit` is omitted and lint uses file `mtime` for decay.

---

## Repository layout

```
.
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── wiki-maintainer/
        ├── plugin.json
        ├── skills/
        │   └── wiki-maintainer/
        │       ├── SKILL.md
        │       └── default-schema.md
        └── commands/
            ├── wiki-init.md
            ├── wiki-ingest.md
            ├── wiki-sync.md
            └── wiki-lint.md
```

---

## Contributing

Issues and PRs welcome. Keep the skill and the four commands in sync — they share assumptions about frontmatter, log format, and decay rules.

---

## License

MIT — see [LICENSE](LICENSE).
