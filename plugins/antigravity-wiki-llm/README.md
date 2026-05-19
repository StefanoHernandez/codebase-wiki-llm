# Antigravity Wiki LLM Pack

Antigravity customization pack for maintaining a living LLM wiki in the current
repository.

This pack mirrors the Codex and Claude Code variants using Antigravity's local
customization model:

- `.agent/rules/codebase-wiki.md` keeps baseline wiki guardrails available.
- `.agent/workflows/wiki-*.md` provides `/wiki-init`, `/wiki-ingest`,
  `/wiki-sync`, and `/wiki-lint` style recipes.
- `.agent/skills/codebase-wiki-maintainer/` contains the reusable skill and
  default schema.
- `GEMINI.md` and `AGENTS.md` are lightweight entrypoints that tell
  Antigravity where to find the pack.

## Global install

From the repository root:

```bash
scripts/install-antigravity-wiki-llm.sh
```

The installer copies files to:

```text
~/.gemini/antigravity/
├── AGENTS.md
├── GEMINI.md
├── global_workflows/
│   ├── wiki-init.md
│   ├── wiki-ingest.md
│   ├── wiki-sync.md
│   └── wiki-lint.md
├── rules/
│   └── codebase-wiki.md
└── skills/
    └── codebase-wiki-maintainer/
        ├── SKILL.md
        └── default-schema.md
```

The installer does not edit `~/.gemini/GEMINI.md` or `~/.gemini/AGENTS.md`.
It keeps this pack under `~/.gemini/antigravity/` so it does not pollute global
Gemini CLI rules.

## Workspace install

For a single project, copy this pack's `.agent/` directory into that project:

```bash
cp -R plugins/antigravity-wiki-llm/.agent /path/to/project/.agent
```

Commit the workspace `.agent/` files when you want the wiki workflows to travel
with the repository.
