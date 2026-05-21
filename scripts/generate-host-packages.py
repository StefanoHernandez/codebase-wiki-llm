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


def main() -> None:
    run("generate-codebase-packages.py")
    run("generate-secondbrain-packages.py")


if __name__ == "__main__":
    main()
