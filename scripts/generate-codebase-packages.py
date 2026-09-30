#!/usr/bin/env python3
"""Generate Codebase Wiki host-specific plugin files."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "canonical" / "codebase"
MARKER_PREFIX = "<!-- Generated from "
INCLUDE_RE = re.compile(r"^\{\{include:([^}]+)\}\}$", re.MULTILINE)

VERSION = (CANONICAL / "VERSION").read_text(encoding="utf-8").strip()

# Everything this generator owns. reset() deletes these before writing so
# files removed from canonical/ also disappear from the host packages.
GENERATED = (
    "plugins/codebase-wiki-llm/.codex-plugin/plugin.json",
    "plugins/codebase-wiki-llm/skills",
    "plugins/codebase-wiki-llm/hooks",
    "plugins/codebase-wiki-llm/scripts",
    "plugins/claude-codebase-wiki-llm/plugin.json",
    "plugins/claude-codebase-wiki-llm/commands",
    "plugins/claude-codebase-wiki-llm/skills",
    "plugins/claude-codebase-wiki-llm/hooks",
    "plugins/claude-codebase-wiki-llm/scripts",
    "plugins/antigravity-codebase-wiki-llm/plugin.json",
    "plugins/antigravity-codebase-wiki-llm/hooks.json",
    "plugins/antigravity-codebase-wiki-llm/rules",
    "plugins/antigravity-codebase-wiki-llm/skills",
    "plugins/antigravity-codebase-wiki-llm/scripts",
    "skills/codebase-wiki-llm",
    "skills/codebase-wiki-context",
    "skills/codebase-wiki-init",
    "skills/codebase-wiki-ingest",
    "skills/codebase-wiki-sync",
    "skills/codebase-wiki-lint",
)


def reset(paths: tuple[str, ...]) -> None:
    for rel in paths:
        path = ROOT / rel
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    for stale in (ROOT / "skills").glob("codebase-*"):
        if stale.is_dir():
            shutil.rmtree(stale)


def read(rel: str) -> str:
    text = (CANONICAL / rel).read_text(encoding="utf-8")
    text = INCLUDE_RE.sub(
        lambda match: (CANONICAL / match.group(1)).read_text(encoding="utf-8").strip(),
        text,
    )
    if "{{" in text:
        raise ValueError(f"unexpanded placeholder in canonical/codebase/{rel}")
    return text.strip() + "\n"


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



WORKFLOWS = {
    "wiki-init": {
        "source": "workflows/wiki-init.md",
        "codex_name": "codebase-wiki-init",
        "title": "Wiki Init",
        "description": "Bootstrap an engineering-first software project wiki in wiki/, .wiki/, or a folder you choose.",
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


REFERENCES = (
    "references/agent-context-template.md",
    "references/agent-handoff-template.md",
    "references/work-tracker-template.md",
    "references/decision-template.md",
    "references/troubleshooting-template.md",
)


CODEBASE_CODEX_PLUGIN_JSON = """{
  "name": "codebase-wiki-llm",
  "version": "@VERSION@",
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
  "hooks": "./hooks/hooks.json",
  "interface": {
    "displayName": "Codebase Wiki LLM",
    "shortDescription": "Maintain per-repo living wikis for codebases.",
    "longDescription": "Codebase Wiki LLM adapts the LLM Wiki pattern to mutable source code. The plugin provides global Codex skills for bootstrapping, ingesting, syncing, and linting a repository-local wiki folder (wiki/ by default, or one you choose such as .wiki/) while keeping every project's wiki content separate.",
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
  "version": "@VERSION@",
  "description": "Bootstrap and maintain a living wiki (wiki/ by default, or a folder you choose such as .wiki/) that stays in sync with source code. Adds /wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint, and a wiki context skill.",
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


HOOK_SCRIPTS = ("scripts/resolve-wiki-root.sh", "scripts/remind-wiki-sync.sh")
PRIVATE_TERMS_SCRIPT = "scripts/check-private-terms.sh"

# Claude Code and Codex read the same hook format; one text, two copies.
SHARED_HOOKS_JSON = r"""{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh \"${CLAUDE_PLUGIN_ROOT}/scripts/resolve-wiki-root.sh\"",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh \"${CLAUDE_PLUGIN_ROOT}/scripts/remind-wiki-sync.sh\" --host claude",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
"""

# Antigravity: named hooks, flat Stop handlers, cwd = the plugin folder.
ANTIGRAVITY_HOOKS_JSON = """{
  "codebase-wiki-sync-reminder": {
    "Stop": [
      {
        "type": "command",
        "command": "sh ./scripts/remind-wiki-sync.sh --host antigravity",
        "timeout": 10
      }
    ]
  }
}
"""


def copy_script(rel: str, dest_dir: str) -> None:
    dest = ROOT / dest_dir / Path(rel).name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CANONICAL / rel, dest)
    dest.chmod(0o755)


def write_hooks(plugin_dir: str) -> None:
    hooks = ROOT / plugin_dir / "hooks/hooks.json"
    hooks.parent.mkdir(parents=True, exist_ok=True)
    hooks.write_text(SHARED_HOOKS_JSON, encoding="utf-8")
    for rel in HOOK_SCRIPTS:
        copy_script(rel, f"{plugin_dir}/scripts")


ANTIGRAVITY_PLUGIN_JSON = """{
  "name": "codebase-wiki-llm",
  "version": "@VERSION@",
  "description": "Bootstrap and maintain a living wiki (wiki/ by default, or a folder you choose such as .wiki/) that stays in sync with source code. Adds /wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint."
}
"""


ANTIGRAVITY_WORKFLOW_TRIGGERS = {
    "wiki-init": "Use when the user says /wiki-init, wiki init, bootstrap wiki, initialize codebase wiki, or asks to start a project wiki.",
    "wiki-ingest": "Use when the user says /wiki-ingest, wiki ingest, document this area in the wiki, or asks to add source knowledge to the codebase wiki.",
    "wiki-sync": "Use when the user says /wiki-sync, wiki sync, update wiki from recent changes, or after a completed coding task in a repo that already has a codebase wiki.",
    "wiki-lint": "Use when the user says /wiki-lint, wiki lint, audit wiki, or check wiki health.",
}


def generate_codex() -> None:
    (ROOT / "plugins/codebase-wiki-llm/.codex-plugin").mkdir(parents=True, exist_ok=True)
    (ROOT / "plugins/codebase-wiki-llm/.codex-plugin/plugin.json").write_text(
        CODEBASE_CODEX_PLUGIN_JSON.replace("@VERSION@", VERSION), encoding="utf-8"
    )
    write_hooks("plugins/codebase-wiki-llm")
    copy_script(PRIVATE_TERMS_SCRIPT, "plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/scripts")
    write(
        "plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "codebase-wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki (wiki/ by default, or the folder named in .wikidir).",
            "maintainer.md",
        ),
    )
    write(
        "plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for ref in REFERENCES:
        write(
            f"plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/{ref}",
            ref,
            read(ref),
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
    (ROOT / "plugins/claude-codebase-wiki-llm").mkdir(parents=True, exist_ok=True)
    (ROOT / "plugins/claude-codebase-wiki-llm/plugin.json").write_text(
        CODEBASE_CLAUDE_PLUGIN_JSON.replace("@VERSION@", VERSION), encoding="utf-8"
    )
    write_hooks("plugins/claude-codebase-wiki-llm")
    copy_script(PRIVATE_TERMS_SCRIPT, "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/scripts")
    write(
        "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki (wiki/ by default, or the folder named in .wikidir).",
            "maintainer.md",
        ),
    )
    write(
        "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for ref in REFERENCES:
        write(
            f"plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/{ref}",
            ref,
            read(ref),
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
    (ROOT / "plugins/antigravity-codebase-wiki-llm").mkdir(parents=True, exist_ok=True)
    (ROOT / "plugins/antigravity-codebase-wiki-llm/plugin.json").write_text(
        ANTIGRAVITY_PLUGIN_JSON.replace("@VERSION@", VERSION), encoding="utf-8"
    )
    (ROOT / "plugins/antigravity-codebase-wiki-llm/hooks.json").write_text(ANTIGRAVITY_HOOKS_JSON, encoding="utf-8")
    for rel in HOOK_SCRIPTS:
        copy_script(rel, "plugins/antigravity-codebase-wiki-llm/scripts")
    copy_script(PRIVATE_TERMS_SCRIPT, "plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/scripts")
    write(
        "plugins/antigravity-codebase-wiki-llm/rules/AGENTS.md",
        "rules/wiki-context.md",
        read("rules/wiki-context.md"),
    )
    write(
        "plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/SKILL.md",
        "maintainer.md",
        skill_content(
            "wiki-maintainer",
            "Knowledge for maintaining an engineering-first software project wiki (wiki/ by default, or the folder named in .wikidir).",
            "maintainer.md",
        ),
    )
    write(
        "plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for ref in REFERENCES:
        write(
            f"plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/{ref}",
            ref,
            read(ref),
        )
    for slug, meta in WORKFLOWS.items():
        description = f"{meta['description']} {ANTIGRAVITY_WORKFLOW_TRIGGERS[slug]}"
        write(
            f"plugins/antigravity-codebase-wiki-llm/skills/{slug}/SKILL.md",
            meta["source"],
            skill_content(slug, description, meta["source"]),
        )


def generate_agent_skills() -> None:
    copy_script(PRIVATE_TERMS_SCRIPT, "skills/codebase-wiki-llm/scripts")
    write(
        "skills/codebase-wiki-llm/SKILL.md",
        "maintainer.md",
        skill_content(
            "codebase-wiki-llm",
            "Use when maintaining a repository-local engineering wiki: its Core map pages, log, work tracker, decisions, and agent handoff.",
            "maintainer.md",
        ),
    )
    write(
        "skills/codebase-wiki-llm/default-schema.md",
        "default-schema.md",
        read("default-schema.md"),
    )
    for ref in REFERENCES:
        write(
            f"skills/codebase-wiki-llm/{ref}",
            ref,
            read(ref),
        )
    write(
        "skills/codebase-wiki-context/SKILL.md",
        "rules/wiki-context.md",
        skill_content(
            "codebase-wiki-context",
            "Use when a repository has a codebase wiki (wiki/, or the folder named in .wikidir) and coding work should read it and keep the log, work tracker, and handoff current.",
            "rules/wiki-context.md",
        ),
    )
    for slug, meta in WORKFLOWS.items():
        write(
            f"skills/codebase-{slug}/SKILL.md",
            meta["source"],
            skill_content(f"codebase-{slug}", meta["description"], meta["source"]),
        )


def main() -> None:
    reset(GENERATED)
    generate_codex()
    generate_claude()
    generate_antigravity()
    generate_agent_skills()


if __name__ == "__main__":
    main()
