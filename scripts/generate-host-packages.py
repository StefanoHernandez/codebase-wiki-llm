#!/usr/bin/env python3
"""Generate host-specific plugin files from canonical wiki prompts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "canonical"
MARKER_PREFIX = "<!-- Generated from "


def read(rel: str) -> str:
    return (CANONICAL / rel).read_text(encoding="utf-8").strip() + "\n"


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
    path.write_text(with_generated_marker(source_rel, content), encoding="utf-8")


def skill_content(name: str, description: str, source_rel: str) -> str:
    return frontmatter([("name", name), ("description", description)]) + read(source_rel)


def command_content(description: str, source_rel: str) -> str:
    return frontmatter([("description", description)]) + read(source_rel)


def workflow_content(title: str, description: str, source_rel: str) -> str:
    return frontmatter([("title", title), ("description", description)]) + read(source_rel)


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


def generate_codex() -> None:
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
    write(
        "plugins/wiki-maintainer/skills/wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki under wiki/.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/wiki-maintainer/skills/wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"plugins/wiki-maintainer/commands/{slug}.md",
            meta["source"],
            command_content(meta["description"], meta["source"]),
        )


def generate_antigravity() -> None:
    write(
        "plugins/antigravity-wiki-llm/.agent/rules/codebase-wiki.md",
        "rules/wiki-context.md",
        rule_content("Wiki context + auto-sync", "rules/wiki-context.md"),
    )
    write(
        "plugins/antigravity-wiki-llm/.agent/skills/codebase-wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki under wiki/.",
            "maintainer.md",
        ),
    )
    write(
        "plugins/antigravity-wiki-llm/.agent/skills/codebase-wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"plugins/antigravity-wiki-llm/.agent/workflows/{slug}.md",
            meta["source"],
            workflow_content(meta["title"], meta["description"], meta["source"]),
        )


def main() -> None:
    generate_codex()
    generate_claude()
    generate_antigravity()


if __name__ == "__main__":
    main()
