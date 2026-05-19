# Project Identity

Codebase Wiki LLM is a multi-host plugin repository for maintaining a per-repository LLM wiki. It packages the same workflow for Codex, Claude Code, and Antigravity while keeping each host's manifest or customization model separate.

# Architecture

- Codex marketplace entry: `.agents/plugins/marketplace.json`
- Claude Code marketplace entry: `.claude-plugin/marketplace.json`
- Antigravity installer: `scripts/install-antigravity-wiki-llm.sh`
- Codex plugin package: `plugins/codebase-wiki-llm`
- Claude Code plugin package: `plugins/wiki-maintainer`
- Antigravity customization pack: `plugins/antigravity-wiki-llm`
- Codex exposes split skills for `/wiki-init`, `/wiki-ingest`, `/wiki-sync`, `/wiki-lint`, context loading, and maintainer rules.
- Claude Code exposes slash commands backed by one `wiki-maintainer` skill.
- Antigravity exposes `GEMINI.md`, `AGENTS.md`, `.agent/rules/`, `.agent/workflows/`, and `.agent/skills/`, installable under `~/.gemini/antigravity/`.
- Generated wikis live in the target project as `<repo>/wiki/`; this repository does not host a global shared wiki.

# Tech Stack

- Markdown-based plugin skills and command definitions.
- JSON marketplace and plugin manifests.
- SVG asset for the Codex plugin icon.
- No application runtime, package manager manifest, or test framework is currently defined.
- Local Python virtual environment: `.venv`.

# Directory Map

- `README.md`: root install and mental-model documentation for both hosts.
- `.agents/plugins/marketplace.json`: Codex marketplace descriptor.
- `.claude-plugin/marketplace.json`: Claude Code marketplace descriptor.
- `plugins/codebase-wiki-llm/.codex-plugin/plugin.json`: Codex plugin manifest.
- `plugins/codebase-wiki-llm/skills/`: Codex split skills.
- `plugins/wiki-maintainer/plugin.json`: Claude Code plugin manifest.
- `plugins/wiki-maintainer/commands/`: Claude Code slash command definitions.
- `plugins/wiki-maintainer/skills/wiki-maintainer/`: Claude Code maintainer skill and schema.
- `plugins/antigravity-wiki-llm/`: Antigravity rules, workflows, skill, and entrypoint files.
- `scripts/install-antigravity-wiki-llm.sh`: Copies the Antigravity pack into the user's Gemini/Antigravity customization directory.
- `scripts/test-antigravity-pack.sh`: Validates required files and tests installation into a temporary HOME.

# Coding Patterns

- Keep host-specific packaging separate instead of forcing one manifest format.
- Keep wiki operations scoped to the target repository's `wiki/` directory.
- During wiki operations, read source files as evidence but do not modify source files.
- Prefer concise, source-grounded Markdown with frontmatter, standard relative links, and Mermaid diagrams where useful.
- Propose deletion or retirement of docs; do not silently delete.

# Known Issues

- `plugins/wiki-maintainer/plugin.json` still points `homepage` and `repository` to `claude-wiki-plugin`, while root documentation points to `codebase-wiki-llm`.
- Codex and Claude default schemas have drifted in wording and dates.
- Lint behavior has a policy tension: some instructions say lint is read-only, while other sections say to append to `wiki/log.md`.
- The repository has no automated verification command beyond JSON syntax validation.

# Roadmap

- Align Claude plugin metadata with the unified repository.
- Decide and document whether `/wiki-lint` may append to `wiki/log.md` or must be strictly read-only.
- Reduce duplication or add a sync process for shared schema text between Codex, Claude, and Antigravity variants.
- Expand lightweight validation beyond the Antigravity pack to all host variants.

# Last Session Log

## 2026-05-19 17:11 CEST - Codex

- Summary: Added a dedicated Antigravity Wiki LLM customization pack with rules, workflows, skill, schema, GEMINI/AGENTS entrypoints, an installer for `~/.gemini/antigravity/`, validation script, and README documentation. Verified install behavior in a temporary HOME.
- Files modified: `README.md`, `plugins/antigravity-wiki-llm/`, `scripts/install-antigravity-wiki-llm.sh`, `scripts/test-antigravity-pack.sh`, `.agent/AI_CONTEXT.md`, `.agent/CHANGELOG.md`, `/Users/stefano/.codex/memories/extensions/ad_hoc/notes/2026-05-19-codebase-wiki-llm-antigravity-pack.md`.

## 2026-05-19 17:02 CEST - Codex

- Summary: Explored how to extend the dual-host wiki plugin model toward Antigravity. Checked local repo state for `.gemini`/Antigravity files and found none in the current checkout. Researched current Antigravity conventions for rules, workflows, and skills to inform a design discussion.
- Files modified: `.agent/AI_CONTEXT.md`, `.agent/CHANGELOG.md`.

## 2026-05-19 16:59 CEST - Codex

- Summary: Synchronized Codebase Wiki LLM project context and operating rules into Codex persistent memory via an ad hoc note.
- Files modified: `.agent/AI_CONTEXT.md`, `.agent/CHANGELOG.md`, `/Users/stefano/.codex/memories/extensions/ad_hoc/notes/2026-05-19-codebase-wiki-llm-project-rules.md`.

## 2026-05-19 16:55 CEST - Codex

- Summary: Analyzed the dual Codex/Claude Code wiki plugin repository, checked packaging, skills, commands, manifests, environment state, and current project risks. Created the required agent context files and local virtual environment.
- Files modified: `.agent/AI_CONTEXT.md`, `.agent/CHANGELOG.md`, `.gitignore`.
