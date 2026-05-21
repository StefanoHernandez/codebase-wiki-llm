#!/usr/bin/env python3
"""Generate SecondBrain host-specific plugin files."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "canonical" / "secondbrain"
MARKER_PREFIX = "<!-- Generated from "


def read(rel: str) -> str:
    return (CANONICAL / rel).read_text(encoding="utf-8").strip() + "\n"


def source(rel: str) -> str:
    return f"secondbrain/{rel}"


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
    "secondbrain-init": {
        "source": "workflows/secondbrain-init.md",
        "codex_name": "secondbrain-init",
        "title": "SecondBrain Init",
        "description": "Bootstrap an adaptive personal and work knowledge vault.",
    },
    "secondbrain-ingest": {
        "source": "workflows/secondbrain-ingest.md",
        "codex_name": "secondbrain-ingest",
        "title": "SecondBrain Ingest",
        "description": "Ingest raw material, inbox notes, files, folders, links, or topics into the vault.",
    },
    "secondbrain-sync": {
        "source": "workflows/secondbrain-sync.md",
        "codex_name": "secondbrain-sync",
        "title": "SecondBrain Sync",
        "description": "Surgically update an existing SecondBrain vault after small changes.",
    },
    "secondbrain-lint": {
        "source": "workflows/secondbrain-lint.md",
        "codex_name": "secondbrain-lint",
        "title": "SecondBrain Lint",
        "description": "Run a read-only health check for a SecondBrain vault.",
    },
}


CODEX_PLUGIN_JSON = """{
  "name": "secondbrain-wiki-llm",
  "version": "0.1.0",
  "description": "Global Codex plugin for maintaining a personal and work knowledge vault.",
  "author": {
    "name": "Stefano"
  },
  "license": "MIT",
  "keywords": [
    "codex",
    "secondbrain",
    "vault",
    "knowledge",
    "markdown",
    "personal-ops"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "SecondBrain Wiki LLM",
    "shortDescription": "Maintain personal and work knowledge vaults.",
    "longDescription": "SecondBrain Wiki LLM maintains adaptive Markdown vaults for projects, work documents, personal documents, meetings, research, tasks, expenses, skills, people, publications, and long-term operational memory.",
    "developerName": "Stefano",
    "category": "Productivity",
    "capabilities": [
      "Read",
      "Write",
      "Project Context"
    ],
    "defaultPrompt": [
      "/secondbrain-init",
      "/secondbrain-ingest raw/",
      "/secondbrain-lint"
    ],
    "brandColor": "#0F766E",
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


CLAUDE_PLUGIN_JSON = """{
  "name": "secondbrain-wiki-llm",
  "version": "0.1.0",
  "description": "Maintain an adaptive personal and work knowledge vault. Adds /secondbrain-init, /secondbrain-ingest, /secondbrain-sync, and /secondbrain-lint.",
  "author": {
    "name": "Stefano Paradisi",
    "url": "https://github.com/StefanoHernandez"
  },
  "homepage": "https://github.com/StefanoHernandez/codebase-wiki-llm",
  "repository": "https://github.com/StefanoHernandez/codebase-wiki-llm",
  "license": "MIT",
  "keywords": ["secondbrain", "vault", "knowledge-base", "skill", "claude-code"]
}
"""


ANTIGRAVITY_PLUGIN_JSON = """{
  "name": "secondbrain-wiki-llm",
  "version": "0.1.0",
  "description": "Maintain an adaptive personal and work knowledge vault. Adds /secondbrain-init, /secondbrain-ingest, /secondbrain-sync, and /secondbrain-lint."
}
"""


ANTIGRAVITY_TRIGGERS = {
    "secondbrain-init": "Use when the user says /secondbrain-init, secondbrain init, initialize second brain, bootstrap vault, or asks to start a personal/work knowledge vault.",
    "secondbrain-ingest": "Use when the user says /secondbrain-ingest, secondbrain ingest, ingest raw material, classify inbox, or add files/links/notes to a vault.",
    "secondbrain-sync": "Use when the user says /secondbrain-sync, secondbrain sync, update vault from recent changes, or asks to refresh existing vault notes.",
    "secondbrain-lint": "Use when the user says /secondbrain-lint, secondbrain lint, audit vault, or check secondbrain health.",
}


def generate_codex() -> None:
    (ROOT / "plugins/secondbrain-wiki-llm/.codex-plugin").mkdir(
        parents=True, exist_ok=True
    )
    (ROOT / "plugins/secondbrain-wiki-llm/.codex-plugin/plugin.json").write_text(
        CODEX_PLUGIN_JSON, encoding="utf-8"
    )
    write(
        "plugins/secondbrain-wiki-llm/skills/secondbrain-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "secondbrain-maintainer",
            "Knowledge for maintaining an adaptive personal and work knowledge vault.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/secondbrain-wiki-llm/skills/secondbrain-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    write(
        "plugins/secondbrain-wiki-llm/skills/secondbrain-context/SKILL.md",
        "rules/secondbrain-context.md",
        skill_content(
            "secondbrain-context",
            "Use a local SecondBrain vault as personal and work knowledge context.",
            "rules/secondbrain-context.md",
        ),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"plugins/secondbrain-wiki-llm/skills/{slug}/SKILL.md",
            meta["source"],
            skill_content(meta["codex_name"], meta["description"], meta["source"]),
        )


def generate_claude() -> None:
    (ROOT / "plugins/claude-secondbrain-wiki-llm").mkdir(parents=True, exist_ok=True)
    (ROOT / "plugins/claude-secondbrain-wiki-llm/plugin.json").write_text(
        CLAUDE_PLUGIN_JSON, encoding="utf-8"
    )
    write(
        "plugins/claude-secondbrain-wiki-llm/skills/secondbrain-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "secondbrain-maintainer",
            "Knowledge for maintaining an adaptive personal and work knowledge vault.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/claude-secondbrain-wiki-llm/skills/secondbrain-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    write(
        "plugins/claude-secondbrain-wiki-llm/skills/secondbrain-context/SKILL.md",
        "rules/secondbrain-context.md",
        skill_content(
            "secondbrain-context",
            "Use a local SecondBrain vault as personal and work knowledge context.",
            "rules/secondbrain-context.md",
        ),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"plugins/claude-secondbrain-wiki-llm/commands/{slug}.md",
            meta["source"],
            command_content(meta["description"], meta["source"]),
        )


def generate_antigravity() -> None:
    (ROOT / "plugins/antigravity-secondbrain-wiki-llm").mkdir(
        parents=True, exist_ok=True
    )
    (ROOT / "plugins/antigravity-secondbrain-wiki-llm/plugin.json").write_text(
        ANTIGRAVITY_PLUGIN_JSON, encoding="utf-8"
    )
    write(
        "plugins/antigravity-secondbrain-wiki-llm/rules/secondbrain.md",
        "rules/secondbrain-context.md",
        rule_content("SecondBrain context", "rules/secondbrain-context.md"),
    )
    write(
        "plugins/antigravity-secondbrain-wiki-llm/skills/secondbrain-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "secondbrain-maintainer",
            "Knowledge for maintaining an adaptive personal and work knowledge vault.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/antigravity-secondbrain-wiki-llm/skills/secondbrain-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for slug, meta in WORKFLOWS.items():
        description = f"{meta['description']} {ANTIGRAVITY_TRIGGERS[slug]}"
        write(
            f"plugins/antigravity-secondbrain-wiki-llm/skills/{slug}/SKILL.md",
            meta["source"],
            skill_content(slug, description, meta["source"]),
        )


def main() -> None:
    generate_codex()
    generate_claude()
    generate_antigravity()


if __name__ == "__main__":
    main()
