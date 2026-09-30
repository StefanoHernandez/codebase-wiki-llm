#!/usr/bin/env python3
"""Validate wiki agent context and handoff pages.

Usage:
  scripts/validate-agent-handoff.py [wiki_dir]

Without wiki_dir it validates the folder named in ./.wikidir, or ./wiki.

The validator is intentionally small and dependency-free. It checks the minimum
contract needed for a new coding agent to continue work from `agent/context.md`
and `agent/handoff.md`.
Sections are found by their <!-- wiki:<id> --> marker, or by the English template heading.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FRONTMATTER = {"title", "updated", "sources", "confidence"}
BATON_HEADING = "## Baton For Next Coding Agent"
TABLE_COLUMNS = [
    "Order",
    "Task",
    "Start files",
    "Done when",
    "Verification command",
    "Notes / blockers",
]
BATON_MARKER = "<!-- wiki:baton -->"
NO_OPEN_WORK = "No open work."
# Context sections: stable marker -> English template heading (fallback for pages without markers).
CONTEXT_SECTIONS = {
    "<!-- wiki:goals -->": "Goals And Non-Goals",
    "<!-- wiki:rules -->": "Non-Negotiable Rules",
    "<!-- wiki:commands -->": "Frequent Commands",
    "<!-- wiki:verified-facts -->": "Verified Facts",
    "<!-- wiki:read-first -->": "Read First",
}
PLACEHOLDER_VALUES = {"", "unknown", "pending", "todo", "tbd", "n/a", "na", "none"}
POINTER_FILE = ".wikidir"
CORE_MAP_ROW = re.compile(r"^\|\s*([a-z-]+)\s*\|\s*`?([^`|]+?)`?\s*\|", re.MULTILINE)
WIKI_ROOT_NAME = re.compile(r"^\.?[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9_-])?$")


def default_wiki_dir(cwd: Path) -> Path:
    pointer = cwd / POINTER_FILE
    if pointer.is_file():
        raw = pointer.read_bytes()
        # PowerShell writes UTF-16 (echo >, Out-File) or UTF-8 with BOM.
        encoding = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"
        lines = [line.strip() for line in raw.decode(encoding).splitlines()]
        value = next((line for line in lines if line), "")
        if WIKI_ROOT_NAME.fullmatch(value):
            return cwd / value
    return cwd / "wiki"


def core_path(wiki_dir: Path, role: str, default: str) -> Path:
    schema = wiki_dir / "SCHEMA.md"
    if schema.is_file():
        for name, value in CORE_MAP_ROW.findall(schema.read_text(encoding="utf-8")):
            value = value.strip()
            if name == role and value and not value.startswith("/") and ".." not in value:
                return wiki_dir / value
    return wiki_dir / default


@dataclass
class Page:
    path: Path
    text: str
    frontmatter: dict[str, object]
    body: str


def parse_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    frontmatter: dict[str, object] = {}
    body = text

    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            raw = text[4:end].splitlines()
            body = text[end + 5 :]
            current_key: str | None = None
            for line in raw:
                if not line.strip():
                    continue
                if line.startswith("  - ") and current_key:
                    frontmatter.setdefault(current_key, [])
                    value = line[4:].strip()
                    if isinstance(frontmatter[current_key], list):
                        frontmatter[current_key].append(value)
                    continue
                if ":" in line and not line.startswith(" "):
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    current_key = key
                    frontmatter[key] = [] if value == "" else value

    return Page(path=path, text=text, frontmatter=frontmatter, body=body)


def validate_frontmatter(page: Page) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FRONTMATTER - set(page.frontmatter))
    if missing:
        errors.append(f"{page.path}: missing frontmatter fields: {', '.join(missing)}")

    sources = page.frontmatter.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{page.path}: frontmatter sources must be a non-empty list")

    confidence = page.frontmatter.get("confidence")
    if confidence not in {"high", "medium", "low"}:
        errors.append(f"{page.path}: confidence must be high, medium, or low")

    return errors


def baton_section(text: str) -> tuple[str | None, bool]:
    """Return the baton section body and whether it was found by its marker."""
    lines = text.splitlines()
    start = by_marker = None
    for i, line in enumerate(lines):
        if line.strip() == BATON_MARKER:
            start, by_marker = i + 1, True
            break
    if start is None:
        for i, line in enumerate(lines):
            if line.strip().startswith(BATON_HEADING):
                start, by_marker = i + 1, False
                break
    if start is None:
        return None, False
    end = next((j for j in range(start, len(lines)) if lines[j].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]), bool(by_marker)


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def is_header(cells: list[str]) -> bool:
    normalized = [cell.lower() for cell in cells]
    return normalized == [column.lower() for column in TABLE_COLUMNS]


def looks_unresolved(value: str) -> bool:
    stripped = value.strip()
    return stripped.lower() in PLACEHOLDER_VALUES or "<" in stripped or ">" in stripped


def has_verification(value: str) -> bool:
    stripped = value.strip()
    lower = stripped.lower()
    if lower.startswith("not verified - "):
        reason = stripped[len("Not verified - ") :].strip()
        return bool(reason) and not looks_unresolved(reason)
    if lower.startswith("not verified"):
        return False
    return not looks_unresolved(stripped)


def validate_handoff(page: Page) -> list[str]:
    section, by_marker = baton_section(page.text)
    if section is None:
        return [f"{page.path}: missing '{BATON_HEADING}' section or '{BATON_MARKER}' marker"]

    rows = table_rows(section)
    if not rows:
        if NO_OPEN_WORK in section:
            return []
        return [f"{page.path}: missing baton table"]

    errors: list[str] = []
    if by_marker:
        header, data_rows = rows[0], rows[1:]
        if len(header) != len(TABLE_COLUMNS):
            errors.append(f"{page.path}: baton table header needs {len(TABLE_COLUMNS)} columns in the fixed order")
    else:
        if not any(is_header(row) for row in rows):
            errors.append(f"{page.path}: baton table header does not match required columns")
        data_rows = [row for row in rows if not is_header(row)]
    if not data_rows and NO_OPEN_WORK in section:
        return errors
    valid_task_rows = 0
    for row in data_rows:
        if len(row) != len(TABLE_COLUMNS):
            errors.append(f"{page.path}: baton row has {len(row)} cells, expected 6")
            continue

        order, task, start_files, done_when, verification, _notes = row
        if not order or not task:
            errors.append(f"{page.path}: baton row missing order or task")
        if looks_unresolved(start_files):
            errors.append(f"{page.path}: task '{task}' missing start files")
        if looks_unresolved(done_when):
            errors.append(f"{page.path}: task '{task}' missing done criteria")
        if not has_verification(verification):
            errors.append(f"{page.path}: task '{task}' missing verification command")
        if (
            not looks_unresolved(start_files)
            and not looks_unresolved(done_when)
            and has_verification(verification)
        ):
            valid_task_rows += 1

    if valid_task_rows == 0:
        errors.append(f"{page.path}: no baton task has start files, done criteria, and verification")

    return errors


def validate_context(page: Page) -> list[str]:
    missing = [
        heading
        for marker, heading in CONTEXT_SECTIONS.items()
        if marker not in page.text and heading not in page.text
    ]
    if missing:
        return [f"{page.path}: context looks too generic; missing: {', '.join(missing)}"]
    return []


def main(argv: list[str]) -> int:
    wiki_dir = Path(argv[1]) if len(argv) > 1 else default_wiki_dir(Path.cwd())
    context_path = core_path(wiki_dir, "context", "agent/context.md")
    handoff_path = core_path(wiki_dir, "handoff", "agent/handoff.md")

    errors: list[str] = []
    for path in (context_path, handoff_path):
        if not path.is_file():
            errors.append(f"{path}: missing required agent continuity page")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    context = parse_page(context_path)
    handoff = parse_page(handoff_path)

    errors.extend(validate_frontmatter(context))
    errors.extend(validate_frontmatter(handoff))
    errors.extend(validate_context(context))
    errors.extend(validate_handoff(handoff))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("agent handoff validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
