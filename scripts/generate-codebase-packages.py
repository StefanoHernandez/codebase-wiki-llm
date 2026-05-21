#!/usr/bin/env python3
"""Generate Codebase Wiki host-specific plugin files."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "canonical" / "codebase"
MARKER_PREFIX = "<!-- Generated from "


def read(rel: str) -> str:
    return (CANONICAL / rel).read_text(encoding="utf-8").strip() + "\n"


def source(rel: str) -> str:
    return f"codebase/{rel}"


def frontmatter(fields: list[tuple[str, str]]) -> str:
    lines = ["---"]
    for key, value in fields:
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def with_generated_marker(source_rel: str, content: str) -> str:
    marker = f"{MARKER_PREFIX}{source_rel}. Do not edit directly. -->\n\n"
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            return content[: end + 5] + "\n" + marker + content[end + 5 :].lstrip()
    return marker + content


def write(path_rel: str, source_rel: str, content: str) -> None:
    path = ROOT / path_rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(with_generated_marker(source(source_rel), content), encoding="utf-8")


def skill_content(name: str, description: str, source_rel: str) -> str:
    return frontmatter([("name", name), ("description", description)]) + read(source_rel)


def command_content(description: str, source_rel: str) -> str:
    return frontmatter([("description", description)]) + read(source_rel)


def rule_content(title: str, source_rel: str) -> str:
    return frontmatter([("title", title), ("activation", "always-on")]) + read(source_rel)


WORKFLOWS = {
    "wiki-init": {
        "source": "workflows/wiki-init.md",
        "codex_name": "codebase-wiki-init",
        "title": "Wiki Init",
        "description": "Bootstrap an engineering-first software project wiki under wiki/.",
    },
    "wiki-ingest": {
        "source": "workflows/wiki-ingest.md",
        "codex_name": "codebase-wiki-ingest",
        "title": "Wiki Ingest",
        "description": "Deep-dive into a file, directory, feature, or topic and update the wiki.",
    },
    "wiki-sync": {
        "source": "workflows/wiki-sync.md",
        "codex_name": "codebase-wiki-sync",
        "title": "Wiki Sync",
        "description": "Surgically sync existing wiki pages after small source or project changes.",
    },
    "wiki-lint": {
        "source": "workflows/wiki-lint.md",
        "codex_name": "codebase-wiki-lint",
        "title": "Wiki Lint",
        "description": "Run a read-only health check for staleness, drift, gaps, and unsupported claims.",
    },
}


CODEBASE_CODEX_PLUGIN_JSON = """{
  "name": "codebase-wiki-llm",
  "version": "0.5.0",
  "description": "Global Codex plugin for maintaining a living LLM wiki for each codebase.",
  "author": {
    "name": "Stefano"
  },
  "license": "MIT",
  "keywords": [
    "codex",
    "wiki",
    "codebase",
    "llm",
    "documentation"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "Codebase Wiki LLM",
    "shortDescription": "Maintain per-repo living wikis for codebases.",
    "longDescription": "Codebase Wiki LLM adapts the LLM Wiki pattern to mutable source code. The plugin provides global Codex skills for bootstrapping, ingesting, syncing, and linting a repository-local wiki/ directory while keeping every project's wiki content separate.",
    "developerName": "Stefano",
    "category": "Productivity",
    "capabilities": [
      "Read",
      "Write",
      "Project Context"
    ],
    "defaultPrompt": [
      "/wiki-init",
      "/wiki-ingest src/",
      "/wiki-lint"
    ],
    "brandColor": "#2563EB",
    "composerIcon": "./assets/icon.svg",
    "logo": "./assets/icon.svg",
    "websiteURL": "https://github.com/StefanoHernandez/codebase-wiki-llm",
    "privacyPolicyURL": "https://github.com/StefanoHernandez/codebase-wiki-llm/blob/main/README.md",
    "termsOfServiceURL": "https://github.com/StefanoHernandez/codebase-wiki-llm/blob/main/LICENSE"
  },
  "homepage": "https://github.com/StefanoHernandez/codebase-wiki-llm",
  "repository": "https://github.com/StefanoHernandez/codebase-wiki-llm"
}
"""


CODEBASE_CLAUDE_PLUGIN_JSON = """{
  "name": "codebase-wiki-llm",
  "version": "0.5.0",
  "description": "Bootstrap and maintain a living wiki under wiki/ that stays in sync with source code. Adds /wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint, and a wiki context skill.",
  "author": {
    "name": "Stefano Paradisi",
    "url": "https://github.com/StefanoHernandez"
  },
  "homepage": "https://github.com/StefanoHernandez/codebase-wiki-llm",
  "repository": "https://github.com/StefanoHernandez/codebase-wiki-llm",
  "license": "MIT",
  "keywords": ["wiki", "documentation", "knowledge-base", "skill", "claude-code"]
}
"""


ANTIGRAVITY_PLUGIN_JSON = """{
  "name": "codebase-wiki-llm",
  "version": "0.5.0",
  "description": "Bootstrap and maintain a living wiki under wiki/ that stays in sync with source code. Adds /wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint."
}
"""


ANTIGRAVITY_WORKFLOW_TRIGGERS = {
    "wiki-init": "Use when the user says /wiki-init, wiki init, bootstrap wiki, initialize codebase wiki, or asks to start a project wiki.",
    "wiki-ingest": "Use when the user says /wiki-ingest, wiki ingest, document this area in the wiki, or asks to add source knowledge to wiki/.",
    "wiki-sync": "Use when the user says /wiki-sync, wiki sync, update wiki from recent changes, or after a completed coding task in a repo that already has wiki/.",
    "wiki-lint": "Use when the user says /wiki-lint, wiki lint, audit wiki, or check wiki health.",
}


def generate_codex() -> None:
    (ROOT / "plugins/codebase-wiki-llm/.codex-plugin/plugin.json").write_text(
        CODEBASE_CODEX_PLUGIN_JSON, encoding="utf-8"
    )
    write(
        "plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "codebase-wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki under wiki/.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    write(
        "plugins/codebase-wiki-llm/skills/codebase-wiki-context/SKILL.md",
        "rules/wiki-context.md",
        skill_content(
            "codebase-wiki-context",
            "Use a repository-local wiki as project context and keep agent continuity current.",
            "rules/wiki-context.md",
        ),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"plugins/codebase-wiki-llm/skills/codebase-wiki-{slug.removeprefix('wiki-')}/SKILL.md",
            meta["source"],
            skill_content(meta["codex_name"], meta["description"], meta["source"]),
        )


def generate_claude() -> None:
    (ROOT / "plugins/claude-codebase-wiki-llm/plugin.json").write_text(
        CODEBASE_CLAUDE_PLUGIN_JSON, encoding="utf-8"
    )
    write(
        "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki under wiki/.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    write(
        "plugins/claude-codebase-wiki-llm/skills/wiki-context/SKILL.md",
        "rules/wiki-context.md",
        skill_content(
            "wiki-context",
            "Use a repository-local wiki as project context and keep agent continuity current.",
            "rules/wiki-context.md",
        ),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"plugins/claude-codebase-wiki-llm/commands/{slug}.md",
            meta["source"],
            command_content(meta["description"], meta["source"]),
        )


def generate_antigravity() -> None:
    (ROOT / "plugins/antigravity-codebase-wiki-llm/plugin.json").write_text(
        ANTIGRAVITY_PLUGIN_JSON, encoding="utf-8"
    )
    write(
        "plugins/antigravity-codebase-wiki-llm/rules/wiki.md",
        "rules/wiki-context.md",
        rule_content("Wiki context + auto-sync", "rules/wiki-context.md"),
    )
    write(
        "plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki under wiki/.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for slug, meta in WORKFLOWS.items():
        description = f"{meta['description']} {ANTIGRAVITY_WORKFLOW_TRIGGERS[slug]}"
        write(
            f"plugins/antigravity-codebase-wiki-llm/skills/{slug}/SKILL.md",
            meta["source"],
            skill_content(slug, description, meta["source"]),
        )


def main() -> None:
    generate_codex()
    generate_claude()
    generate_antigravity()


if __name__ == "__main__":
    main()
