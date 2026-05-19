# Antigravity Wiki LLM

Use the Codebase Wiki LLM Antigravity pack when the user asks to initialize,
ingest, sync, lint, or consult a repository-local wiki.

Pack locations after global install:

- Skill: `~/.gemini/antigravity/skills/codebase-wiki-maintainer/SKILL.md`
- Workflows: `~/.gemini/antigravity/global_workflows/wiki-*.md`
- Rules: `~/.gemini/antigravity/rules/codebase-wiki.md`

Core rule: wiki operations may read source files as evidence, but they write
only under the current repository's `wiki/` directory unless the user explicitly
asks for a different project change.
