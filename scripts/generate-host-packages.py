#!/usr/bin/env python3
"""Generate all host-specific plugin files."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script_name: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name)],
        cwd=ROOT,
        check=True,
    )


MARKETPLACE = """{
  "name": "stefano-wiki",
  "description": "Wiki plugins for codebase documentation and personal/work knowledge vaults.",
  "owner": {
    "name": "Stefano Paradisi",
    "url": "https://github.com/StefanoHernandez"
  },
  "plugins": [
    {
      "name": "codebase-wiki-llm",
      "source": "./plugins/claude-codebase-wiki-llm",
      "description": "Maintain a living, LLM-owned wiki of a codebase (wiki/ by default, or a folder you choose such as .wiki/). Adds /wiki-init, /wiki-ingest, /wiki-sync, /wiki-lint, and a wiki context skill.",
      "version": "@CODEBASE_VERSION@"
    },
    {
      "name": "secondbrain-wiki-llm",
      "source": "./plugins/claude-secondbrain-wiki-llm",
      "description": "Maintain an adaptive personal and work knowledge vault. Adds /secondbrain-init, /secondbrain-ingest, /secondbrain-sync, and /secondbrain-lint.",
      "version": "@SECONDBRAIN_VERSION@"
    }
  ]
}
"""


def version(plugin: str) -> str:
    return (ROOT / "canonical" / plugin / "VERSION").read_text(encoding="utf-8").strip()


def main() -> None:
    run("generate-codebase-packages.py")
    run("generate-secondbrain-packages.py")
    (ROOT / ".claude-plugin/marketplace.json").write_text(
        MARKETPLACE.replace("@CODEBASE_VERSION@", version("codebase")).replace(
            "@SECONDBRAIN_VERSION@", version("secondbrain")
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
