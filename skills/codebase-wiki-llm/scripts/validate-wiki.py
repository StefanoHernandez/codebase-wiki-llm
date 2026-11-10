#!/usr/bin/env python3
"""Read-only structural lint of the documented Codebase Wiki format (Python 3.10+).

Usage: python3 <maintainer>/scripts/validate-wiki.py <wiki-root>
Exit 0: valid structure; 1: findings; 2: invocation/configuration error.
This is a small format checker, not a general YAML or Markdown parser. It does
not inspect private terms, verify claims, run commands, or alter any files.
"""
from __future__ import annotations

import datetime
import fnmatch
import json
import re
import string
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULTS = {
    "index": "index.md", "log": "log.md", "tracker": "project/work-tracker.md",
    "decisions": "project/decisions.md", "risks": "project/risks.md",
    "context": "agent/context.md", "handoff": "agent/handoff.md",
    "troubleshooting": "engineering/troubleshooting.md", "glossary": "glossary.md",
}
CONTEXT = {
    "goals": "Goals And Non-Goals", "rules": "Non-Negotiable Rules",
    "commands": "Frequent Commands", "verified-facts": "Verified Facts",
    "read-first": "Read First",
}
HANDOFF = {
    "state": "Current Work State", "baton": "Baton For Next Coding Agent",
    "blockers": "Blockers", "risks": "Known Risks", "commands-run": "Commands Already Run",
    "do-not-redo": "Do Not Redo", "evidence-trail": "Evidence Trail",
}
TRACKER = {"open": "Open", "proposals": "Proposals", "done": "Done"}
BATON_COLUMNS = ["Order", "Task", "Start files", "Done when", "Verification command", "Notes / blockers"]
OPEN_COLUMNS = ["ID", "Status", "Goal", "Done when", "Owner", "Next verification", "Evidence"]
DONE_COLUMNS = ["ID", "Status", "Goal", "Closed", "Criteria met", "Evidence"]
UNRESOLVED = {"", "unknown", "pending", "todo", "tbd", "n/a", "na", "none"}
HTML_TAGS = "br|sub|sup|kbd|code|em|strong|b|i|u|s|del|ins|mark|span|details|summary"
# A placeholder is <text> that is not glued to a word (Vec<u8>), not an autolink and not inline HTML.
PLACEHOLDER = re.compile(
    rf"(?<!\w)<(?!/?(?:{HTML_TAGS})\b)(?![A-Za-z][A-Za-z0-9+.-]{{1,31}}:[^\s<>]*>)(?![^\s<>@]+@[^\s<>]+>)[^<>]+>")
# The validator is installed on its own, so it carries both numbers.
# VERSION is the plugin release; it equals canonical/codebase/VERSION.
VERSION = "0.13.0"
# FORMAT_VERSION is the wiki format this validator checks. Raise it only when a
# release adds an `upgrade:` check or changes a structure tools read.
FORMAT_VERSION = "0.12.0"
SCHEMA_SECTIONS = ["Project profile", "Conventions", "Evidence", "Confidentiality", "Budgets",
                   "Log format", "Topics", "Page frontmatter"]
DECISION_STATUS = re.compile(r"(proposed|accepted|rejected|superseded by \d{4})")
OWNERS_COLUMNS = ["Topic", "Owner page"]
RISK_COLUMNS = ["ID", "Risk", "Severity", "Trigger", "Mitigation", "Owner", "IDs"]
RISK_SEVERITY = {"critical", "high", "medium", "low"}


def version_tuple(value: str) -> tuple[int, ...] | None:
    return tuple(int(p) for p in value.split(".")) if re.fullmatch(r"\d+(?:\.\d+){2}", value) else None


def columns_match(header: list[str], expected: list[str]) -> bool:
    """English column names must be exact and in order; a translated header only keeps the count."""
    return header == expected if set(header) & set(expected) else len(header) == len(expected)


def unresolved(value: str) -> bool:
    value = value.strip().strip("`").strip()
    return value.lower() in UNRESOLVED or bool(PLACEHOLDER.search(value))


def iso_date(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def private_terms_path(path: Path) -> bool:
    return ".private-terms" in path.parts or ".private-terms" in path.resolve().parts


def explicit_unproven(value: str) -> bool:
    """Recognize a cell's fixed negative claim, not prose discussing one."""
    value = value.strip()
    return bool(re.match(
        r"^(?:>\s*)?(?:⚠\ufe0f?\s*)?(?:not verified(?:\s*-|\s*$)|not proven:)"
        r"|^closed by .+? \d{4}-\d{2}-\d{2}; not proven:", value, re.I,
    ))


def unfenced(lines: list[str]) -> list[str]:
    """Blank fenced examples while retaining original diagnostic line numbers."""
    out = []
    fence = None
    for line in lines:
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
            out.append("")
        elif match:
            fence = match[1]
            out.append("")
        else:
            out.append(line)
    return out


def inline_destinations(line: str) -> list[str]:
    """Read ordinary inline destinations, balancing parentheses and escapes."""
    destinations = []
    for match in re.finditer(r"!?\[[^\]]*\]\(", line):
        pos = match.end()
        while pos < len(line) and line[pos].isspace():
            pos += 1
        angle = pos < len(line) and line[pos] == "<"
        if angle:
            pos += 1
        value = []
        depth = 0
        while pos < len(line):
            char = line[pos]
            if char == "\\" and pos + 1 < len(line) and line[pos + 1] in string.punctuation:
                value.append(line[pos + 1])
                pos += 2
                continue
            if angle:
                if char == ">":
                    break
            elif char.isspace() or (char == ")" and depth == 0):
                break
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            value.append(char)
            pos += 1
        if pos == len(line) or depth or (angle and line[pos] != ">"):
            continue
        if angle:
            pos += 1
        end = pos
        while pos < len(line) and line[pos].isspace():
            pos += 1
        # A title must be separated from the destination by whitespace.
        if pos > end and pos < len(line) and line[pos] in "\"'(":
            closing = ")" if line[pos] == "(" else line[pos]
            pos += 1
            while pos < len(line) and line[pos] != closing:
                pos += 2 if line[pos] == "\\" and pos + 1 < len(line) else 1
            if pos == len(line):
                continue
            pos += 1
            while pos < len(line) and line[pos].isspace():
                pos += 1
        if pos < len(line) and line[pos] == ")":
            destinations.append("".join(value))
    return destinations


@dataclass
class Note:
    path: Path | None
    line: int | None
    message: str
    code: str = ""
    fix: str = ""  # upgrades only: "adopt" or "update-plugin"


@dataclass
class Page:
    path: Path
    lines: list[str]
    fields: dict[str, str | list[str]]
    locations: dict[str, int]
    has_frontmatter: bool


class Validator:
    def __init__(self, wiki: Path):
        self.wiki = wiki.resolve()
        # Sources belong to the target repository, never the installed package.
        self.repo = next((p for p in self.wiki.parents if (p / ".git").exists()), self.wiki.parent)
        self.findings: list[Note] = []
        self.infos: list[Note] = []
        # What is still missing for the current format: reported, never a finding.
        self.upgrades: list[Note] = []
        self.tracker_ids: set[str] | None = None
        self.pages: dict[Path, Page] = {}

    def error(self, path: Path, line: int, message: str):
        self.findings.append(Note(path, line, message))

    def upgrade(self, path: Path, line: int, code: str, message: str, fix: bool = True):
        self.upgrades.append(Note(path, line, message, code, "adopt" if fix else "update-plugin"))

    def info(self, code: str, message: str, path: Path | None = None, line: int | None = None):
        self.infos.append(Note(path, line, message, code))

    def root(self) -> str:
        try:
            return self.wiki.relative_to(self.repo).as_posix()
        except ValueError:
            return str(self.wiki)

    def rel(self, path: Path | None) -> str | None:
        if path is None:
            return None
        try:
            return path.relative_to(self.wiki).as_posix()
        except ValueError:
            return str(path)

    def report(self, code: int) -> dict:
        def row(note: Note, *extra: str) -> dict:
            out = {"path": self.rel(note.path), "line": note.line}
            out.update({key: getattr(note, key) for key in extra})
            out["message"] = note.message
            return out
        return {"validator": VERSION, "format": FORMAT_VERSION, "wiki": self.root(), "exit": code, "error": None,
                "findings": [row(n) for n in self.findings],
                "upgrades": [dict(row(n, "code"), fix=n.fix) for n in self.upgrades],
                "infos": [row(n, "code") for n in self.infos]}

    def load(self, path: Path):
        try:
            self.read_page(path)
        except (OSError, UnicodeError):
            self.error(path, 1, "cannot read page (unreadable or not UTF-8)")

    @staticmethod
    def marked(page: Page, marker: str) -> bool:
        return any(line.strip() == f"<!-- wiki:{marker} -->" for line in page.lines)

    def read_page(self, path: Path) -> Page:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        fields: dict[str, str | list[str]] = {}
        locations: dict[str, int] = {}
        end = 0
        if lines and lines[0] == "---" and "---" in lines[1:]:
            end = lines.index("---", 1)
            current = ""
            for number, line in enumerate(lines[1:end], 2):
                if not line.strip():
                    continue
                item = re.fullmatch(r"  - (.+)", line)
                scalar = re.fullmatch(r"([a-z_]+):(?: (.*))?", line)
                if item and current == "sources" and isinstance(fields.get(current), list):
                    fields[current].append(self.scalar(item[1], path, number))
                elif scalar:
                    current = scalar[1]
                    value = (scalar[2] or "").strip()
                    if value.startswith(("[", "{", "|", ">", "&", "*", "!")) and current not in ("generated", "verified"):
                        self.error(path, number, "unsupported frontmatter value; use a plain or quoted scalar (sources uses an indented list)")
                    if current in fields:
                        self.error(path, number, f"duplicate frontmatter key {current}")
                    fields[current] = [] if current == "sources" and not scalar[2] else self.scalar(scalar[2] or "", path, number)
                    locations[current] = number
                else:
                    self.error(path, number, "unsupported frontmatter structure; use scalar fields and an indented sources list")
        else:
            self.error(path, 1, "missing or unterminated frontmatter")
        body = [""] * (end + 1) + lines[end + 1:] if end else lines
        page = Page(path, unfenced(body), fields, locations, bool(end))
        self.pages[path] = page
        return page

    def scalar(self, value: str, path: Path, line: int) -> str:
        value = value.strip()
        if value.startswith(("\"", "'")):
            escaped_end = value[0] == '"' and (len(value[:-1]) - len(value[:-1].rstrip("\\"))) % 2 == 1
            if len(value) < 2 or value[-1] != value[0] or escaped_end:
                self.error(path, line, "unterminated quoted frontmatter scalar")
            else:
                return value[1:-1].strip()
        return value

    def frontmatter(self, page: Page):
        # One root finding already identifies missing/unterminated metadata.
        # Links and role-specific checks still run on this page's body.
        if not page.has_frontmatter:
            return
        schema = page.path == self.wiki / "SCHEMA.md"
        required = {"title", "confidence"} | (set() if schema else {"sources", "source_commit"})
        for key in sorted(required - page.fields.keys()):
            self.error(page.path, 1, f"missing frontmatter field {key}")
        if not ({"updated", "generated"} & page.fields.keys()):
            self.error(page.path, 1, "missing frontmatter field updated or generated")
        for key in ("title", "source_commit"):
            if key in page.fields and (not isinstance(page.fields[key], str) or not page.fields[key]):
                self.error(page.path, page.locations[key], f"{key} must be non-empty")
        if "updated" in page.fields and not iso_date(str(page.fields.get("updated", ""))):
            self.error(page.path, page.locations.get("updated", 1), "updated must be a real ISO date YYYY-MM-DD")
        if page.fields.get("confidence") not in ("high", "medium", "low"):
            self.error(page.path, page.locations.get("confidence", 1), "confidence must be high, medium, or low")
        if "sources" not in page.fields and schema:
            return
        sources = page.fields.get("sources")
        line = page.locations.get("sources", 1)
        if not isinstance(sources, list) or not sources:
            self.error(page.path, line, "sources must be a non-empty indented list of repository-relative paths")
            return
        for offset, source in enumerate(sources, 1):
            raw = re.sub(r":\d+(?::\d+)?$", "", source.split("#", 1)[0])
            target = self.repo / raw
            if not raw or unresolved(source) or Path(raw).is_absolute() or not target.resolve().is_relative_to(self.repo) or not target.exists():
                # Do not echo the source value (which might contain private terms).
                self.error(page.path, line + offset, "source must name an existing repository-relative file or directory; resolve placeholders")

    def section(self, page: Page, marker: str, heading: str, required=True):
        token = f"<!-- wiki:{marker} -->"
        starts = [i for i, line in enumerate(page.lines) if line.strip() == token]
        if len(starts) > 1:
            self.error(page.path, starts[1] + 1, f"duplicate {token} section")
        if starts:
            start = starts[0]
            if not start or not page.lines[start - 1].startswith("## "):
                self.error(page.path, start + 1, f"{token} must be directly under its section heading")
        else:
            start = next((i for i, line in enumerate(page.lines) if line.strip() == f"## {heading}"), None)
        if start is None:
            if required:
                self.error(page.path, 1, f"missing section {token} (or legacy English heading '{heading}')")
            return []
        end = next((i for i in range(start + 1, len(page.lines)) if page.lines[i].startswith("## ")), len(page.lines))
        return [(i + 1, page.lines[i]) for i in range(start + 1, end)]

    def table(self, page: Page, section):
        rows = []
        for number, line in section:
            cells = re.split(r"(?<!\\)\|", line.strip())
            if len(cells) > 1:
                # Outer delimiters are optional; preserve empty interior cells.
                if cells[0] == "":
                    cells.pop(0)
                if cells[-1] == "":
                    cells.pop()
                cells = [cell.strip() for cell in cells]
                rows.append((number, cells))
        if not rows:
            return []
        # The immediate delimiter identifies the header, not earlier pipe prose.
        # Keep the first candidate as a fallback so malformed tables still fail.
        start = next((i for i in range(len(rows) - 1)
                      if rows[i + 1][0] == rows[i][0] + 1
                      and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[i + 1][1])), 0)
        rows = rows[start:]
        if (len(rows) < 2 or rows[1][0] != rows[0][0] + 1
                or len(rows[1][1]) != len(rows[0][1])
                or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1][1])):
            self.error(page.path, rows[0][0], "table header needs a matching Markdown delimiter immediately below it")
            return []
        # A blank line ends this table region; later prose is not another row.
        end = next((number for number, line in section
                    if number > rows[0][0] and not line.strip()), section[-1][0] + 1)
        rows = [row for row in rows if row[0] < end]
        row_numbers = {number for number, _cells in rows}
        for number, line in section:
            if rows[0][0] < number < end and number not in row_numbers and line.strip():
                self.error(page.path, number, "unsupported table row; use pipe-separated cells matching the header")
        return [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row[1])]

    def core_map(self, schema: Page):
        section = self.section(schema, "core-map", "Core map", required=False)
        if not section:
            # A present but empty map must not masquerade as a v1 wiki.
            if any(l.strip() in ("## Core map", "<!-- wiki:core-map -->") for l in schema.lines):
                self.error(schema.path, 1, "Core map is empty")
                return {}
            mapping = DEFAULTS.copy()
        else:
            mapping = {}
            rows = self.table(schema, section)
            if not rows or rows[0][1] != ["Role", "Path"]:
                self.error(schema.path, 1, "unsupported Core map table; expected Role and Path columns")
            for number, cells in rows[1:]:
                if len(cells) != 2:
                    self.error(schema.path, number, "Core map row needs Role and Path")
                    continue
                role, raw = cells
                value = raw.strip("`")
                if role in mapping:
                    self.error(schema.path, number, f"duplicate Core map role {role}")
                if role not in {*DEFAULTS, "log-archive", "activity (v1)"}:
                    self.error(schema.path, number, "unsupported Core map role")
                target = self.wiki / value
                if unresolved(value) or Path(value).is_absolute() or ".." in Path(value).parts or not target.resolve().is_relative_to(self.wiki) or private_terms_path(target):
                    self.error(schema.path, number, "unsafe Core map path; paths must stay inside the wiki")
                    continue
                mapping[role] = value
            for role in sorted({*DEFAULTS, "log-archive"} - mapping.keys()):
                self.error(schema.path, 1, f"Core map missing required role {role}")
        paths = {}
        for role, value in mapping.items():
            target = self.wiki / value
            is_dir = role == "log-archive"
            valid_kind = target.is_dir() if is_dir else target.is_file()
            kind = "directory" if is_dir else "file"
            if is_dir and not target.exists() and not target.is_symlink():
                # The archive is a reservation until the first archive write.
                # A file or dangling symlink in its ancestry cannot be created
                # through; an outside symlink is rejected by the boundary check.
                valid_kind = all(parent.is_dir() or not (parent.exists() or parent.is_symlink())
                                 for parent in target.parents if parent.is_relative_to(self.wiki))
                kind = "directory or creatable reserved path"
            # Adoption maps a v1 decisions file in place before any optional split.
            if role == "decisions" and section:
                valid_kind = target.is_file() or target.is_dir()
                kind = "file or directory"
            if private_terms_path(target) or not target.resolve().is_relative_to(self.wiki) or not valid_kind:
                self.error(schema.path, 1, f"Core map {role} must point to an existing {kind} inside the wiki")
            else:
                paths[role] = target
        return paths

    def glob_ok(self, schema: Page, number: int, glob: str, what: str) -> bool:
        if not glob or Path(glob).is_absolute() or ".." in Path(glob).parts:
            self.error(schema.path, number, f"unsafe {what} glob; use a wiki-relative pattern without ..")
            return False
        return True

    def excluded(self, schema: Page, paths: dict[str, Path]) -> list[str]:
        # Only bullets are rules; prose explaining the section is ignored.
        globs = []
        for number, line in self.section(schema, "excluded-paths", "Excluded paths", required=False):
            if not line.startswith("- "):
                continue
            entry = re.fullmatch(r"- `([^`]+)`", line.strip())
            if not entry:
                self.error(schema.path, number, "Excluded paths entry must be - `<glob>`")
            elif self.glob_ok(schema, number, entry[1], "Excluded paths"):
                globs.append((number, entry[1]))
        protected = [p.relative_to(self.wiki).as_posix() for p in (schema.path, *paths.values()) if p.is_file()]
        kept = []
        for number, glob in globs:
            if any(fnmatch.fnmatchcase(rel, glob) for rel in protected):
                self.error(schema.path, number, "Excluded paths must not match SCHEMA or Core map pages")
            else:
                kept.append(glob)
        return kept

    def page_types(self, schema: Page):
        # Shape only: page `type` values are the lint's concern.
        rows = self.table(schema, self.section(schema, "page-types", "Page types", required=False))
        if not rows:
            return
        if rows[0][1] != ["Path", "type"]:
            self.error(schema.path, rows[0][0], "unsupported Page types table; expected Path and type columns")
            return
        for number, cells in rows[1:]:
            if len(cells) != 2 or unresolved(cells[1].strip("`")):
                self.error(schema.path, number, "Page types row needs a glob and a type")
                continue
            self.glob_ok(schema, number, cells[0].strip("`"), "Page types")

    def links(self, page: Page):
        for number, line in enumerate(page.lines, 1):
            line = re.sub(r"(`+).*?\1", "", line)
            links = inline_destinations(line)
            # Standard reference definitions are checked too; no arbitrary Markdown extensions.
            reference = re.match(r"^ {0,3}\[(?!\^)[^\]]+\]:\s*(<[^>]+>|\S+)", line)
            if reference:
                links.append(reference[1].strip("<>"))
            for link in links:
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                path = unquote(url.path)
                target = page.path.parent / path
                if Path(path).is_absolute() or not target.resolve().is_relative_to(self.repo) or not target.exists():
                    self.error(page.path, number, "broken or unsafe relative Markdown link")

    def tracker(self, page: Page):
        ids = set()
        open_ids = set()
        open_readable = True
        ids_readable = True
        for kind, heading in TRACKER.items():
            before = len(self.findings)
            section = self.section(page, kind, heading)
            rows = self.table(page, section)
            if kind == "open" and len(self.findings) != before:
                open_readable = False
            if not rows:
                if len(self.findings) == before:
                    self.error(page.path, 1, f"missing {kind} tracker table")
                if kind == "open":
                    open_readable = False
                if kind == "done":
                    ids_readable = False
                continue
            header = rows[0][1]
            if kind == "proposals":
                for number, cells in rows[1:]:
                    if re.fullmatch(r"T[1-9]\d*", cells[0]) or any(cell in ("🟢", "⚫", "🟡", "⚪", "🔴") for cell in cells):
                        self.error(page.path, number, "proposal must not define an activity ID or status icon")
                continue
            columns = OPEN_COLUMNS if kind == "open" else DONE_COLUMNS
            legacy = kind == "done" and "Status" not in header and len(header) == 5
            if legacy:
                columns = [c for c in columns if c != "Status"]
                # Legacy rows stay valid; only a new ⚫ closure has nowhere to go.
                self.upgrade(page.path, rows[0][0], "done-status-missing", "Done table has no Status column; ⚫ closures cannot be recorded")
            # Marked translated tables keep the documented column order.
            if all(c in header for c in columns):
                positions = {c: header.index(c) for c in columns}
            elif len(header) >= len(columns) and any(line.strip() == f"<!-- wiki:{kind} -->" for line in page.lines):
                positions = {c: i for i, c in enumerate(columns)}
            else:
                self.error(page.path, rows[0][0], f"unsupported {kind} tracker columns")
                if kind == "open":
                    open_readable = False
                ids_readable = False
                continue
            for number, cells in rows[1:]:
                if len(cells) != len(header):
                    msg = f"{kind} tracker row does not match its header"
                    if len(cells) > len(header):
                        msg += r" (a literal | inside a cell is written \|)"
                    self.error(page.path, number, msg)
                    if kind == "open":
                        open_readable = False
                    ids_readable = False
                    continue
                row = {c: cells[i] for c, i in positions.items()}
                activity = row["ID"]
                if not re.fullmatch(r"T[1-9]\d*", activity):
                    self.error(page.path, number, "tracker ID must be T followed by a positive integer")
                    if kind == "open":
                        open_readable = False
                    ids_readable = False
                if activity in ids:
                    self.error(page.path, number, f"duplicate tracker ID {activity}")
                ids.add(activity)
                for column in ("Goal", "Evidence", "Done when", "Next verification") if kind == "open" else ("Goal", "Closed", "Criteria met", "Evidence"):
                    if unresolved(row[column]):
                        self.error(page.path, number, f"{kind} row needs {column.lower()}")
                if kind == "open":
                    open_ids.add(activity)
                    if row["Status"] not in ("🟡", "⚪", "🔴"):
                        self.error(page.path, number, "open tracker status must be 🟡, ⚪, or 🔴")
                    continue
                status = row.get("Status", "🟢")
                if status not in ("🟢", "⚫"):
                    self.error(page.path, number, "terminal tracker status must be 🟢 or ⚫")
                if not iso_date(row["Closed"]):
                    self.error(page.path, number, "Closed must be a real ISO date")
                if status == "🟢" and any(explicit_unproven(row[column]) for column in ("Criteria met", "Evidence")):
                    self.error(page.path, number, "green row contains an explicit unproven claim in criteria or evidence")
                if status == "⚫":
                    closure = re.fullmatch(r"closed by (.+?) (\d{4}-\d{2}-\d{2}); not proven: (.+)", row["Criteria met"], re.I)
                    if not closure or unresolved(closure[1]) or unresolved(closure[3]) or closure[1].lower() in ("agent", "coding agent", "ai"):
                        self.error(page.path, number, "black row needs 'closed by <person> YYYY-MM-DD; not proven: <what>' and human closure evidence")
                    elif not iso_date(closure[2]):
                        self.error(page.path, number, "black row has invalid closure date")
        if open_readable and ids_readable:
            self.tracker_ids = ids
        return open_ids if open_readable else None

    def format_upgrades(self, schema: Page, paths: dict[str, Path], has_core_map: bool):
        """Report what a wiki still needs for the current format, without failing it."""
        declared = schema.fields.get("format_version")
        line = schema.locations.get("format_version", 1)
        if not isinstance(declared, str) or not declared:
            self.upgrade(schema.path, 1, "format-version-missing", "format_version missing")
        elif version_tuple(declared) is None:
            self.upgrade(schema.path, line, "format-version-invalid", "format_version must be X.Y.Z")
        elif version_tuple(declared) < version_tuple(FORMAT_VERSION):
            self.upgrade(schema.path, line, "format-version-older", f"format_version {declared} is older than {FORMAT_VERSION}")
        elif version_tuple(declared) > version_tuple(FORMAT_VERSION):
            self.upgrade(schema.path, line, "format-version-newer", f"format_version {declared} is newer than this plugin ({FORMAT_VERSION}); update the plugin", fix=False)
            # An older plugin must not propose edits to a newer wiki.
            return
        if not has_core_map:
            self.upgrade(schema.path, 1, "core-map-missing", "Core map missing (v1 wiki)")
        for name in SCHEMA_SECTIONS:
            slug = name.lower().replace(" ", "-")
            if f"## {name}" not in (l.strip() for l in schema.lines) and not self.marked(schema, slug):
                self.upgrade(schema.path, 1, "schema-section-missing", f"SCHEMA section ## {name} (or <!-- wiki:{slug} -->) missing")
        decisions = paths.get("decisions")
        if decisions is not None and decisions.is_file():
            self.upgrade(schema.path, 1, "decisions-not-folder", "decisions must be a folder of NNNN-<slug>.md files")
        elif decisions is not None:
            for path in sorted(decisions.glob("*.md")):
                page = self.pages.get(path)
                if not page or not re.fullmatch(r"\d{4}-.+\.md", path.name):
                    continue
                status = page.fields.get("status")
                if not isinstance(status, str) or not status:
                    self.upgrade(path, 1, "decision-status-missing", "decision status must be in frontmatter (status: proposed | accepted | rejected | superseded by NNNN)")
                elif not DECISION_STATUS.fullmatch(status):
                    self.upgrade(path, page.locations.get("status", 1), "decision-status-invalid", "decision status must be proposed, accepted, rejected or superseded by NNNN")
                if "## Approval" not in (l.strip() for l in page.lines) and not self.marked(page, "approval"):
                    self.upgrade(path, 1, "decision-approval-missing", "decision has no ## Approval section (or <!-- wiki:approval -->)")

    def cited_ids(self, page: Page, number: int, text: str, what: str):
        text = re.sub(r"(`+).*?\1", "", text)
        if self.tracker_ids is None:
            if re.search(r"\bT[1-9]\d*\b", text):
                self.error(page.path, number, f"{what} tracker references not checked: tracker IDs are unavailable")
            return
        for activity in re.findall(r"\bT[1-9]\d*\b", text):
            if activity not in self.tracker_ids:
                self.error(page.path, number, f"{what} cites unknown tracker ID {activity}")

    def owners(self, page: Page):
        if not self.marked(page, "owners"):
            return
        rows = self.table(page, self.section(page, "owners", "How this wiki is organised"))
        if not rows or not columns_match(rows[0][1], OWNERS_COLUMNS):
            self.error(page.path, rows[0][0] if rows else 1, "unsupported owners table; expected Topic and Owner page columns")
            return
        for number, cells in rows[1:]:
            if len(cells) != 2 or unresolved(cells[0]) or "](" not in cells[1]:
                self.error(page.path, number, "owners row needs a topic and an owner page link")

    def next_steps(self, page: Page):
        if self.marked(page, "next"):
            for number, line in self.section(page, "next", "Next steps"):
                self.cited_ids(page, number, line, "Next steps")

    def risk_register(self, page: Page):
        if not self.marked(page, "risk-register"):
            return
        rows = self.table(page, self.section(page, "risk-register", "Register"))
        if not rows or not columns_match(rows[0][1], RISK_COLUMNS):
            self.error(page.path, rows[0][0] if rows else 1, "unsupported risk register table; expected " + " | ".join(RISK_COLUMNS))
            return
        seen = set()
        for number, cells in rows[1:]:
            if len(cells) != len(RISK_COLUMNS):
                self.error(page.path, number, "risk register row does not match its header")
                continue
            risk = dict(zip(RISK_COLUMNS, cells))
            if not re.fullmatch(r"R[1-9]\d*", risk["ID"]):
                self.error(page.path, number, "risk ID must be R followed by a positive integer")
            elif risk["ID"] in seen:
                self.error(page.path, number, f"duplicate risk ID {risk['ID']}")
            seen.add(risk["ID"])
            if risk["Severity"].strip("`") not in RISK_SEVERITY:
                self.error(page.path, number, "risk severity must be critical, high, medium or low")
            for column in ("Risk", "Trigger", "Mitigation"):
                if unresolved(risk[column]):
                    self.error(page.path, number, f"risk row needs {column.lower()}")
            self.cited_ids(page, number, risk["IDs"], "risk")

    def handoff(self, page: Page, open_ids: set[str] | None):
        if open_ids is None:
            self.error(page.path, 1, "handoff tracker references not checked: Open tracker IDs are unavailable")
        sections = {marker: self.section(page, marker, heading) for marker, heading in HANDOFF.items()}
        baton = sections["baton"]
        rows = self.table(page, baton)
        no_work = any(line.strip() == "No open work." for _, line in baton)
        if no_work and open_ids:
            line = next(number for number, text in baton if text.strip() == "No open work.")
            self.info("handoff-no-open-work-stale",
                      "handoff says No open work. but the tracker has open rows; refresh the handoff with /wiki-sync",
                      page.path, line)
        if no_work and len(rows) > 1:
            self.error(page.path, 1, "No open work. contradicts baton task rows")
        if not rows:
            if not no_work:
                self.error(page.path, 1, "missing baton table or No open work.")
            return
        header = rows[0][1]
        marked = any(line.strip() == "<!-- wiki:baton -->" for line in page.lines)
        if len(header) != 6 or (not marked and header != BATON_COLUMNS) or (set(header) == set(BATON_COLUMNS) and header != BATON_COLUMNS):
            self.error(page.path, rows[0][0], "baton table needs six columns in the documented order")
        if len(rows) == 1 and not no_work:
            self.error(page.path, rows[0][0], "baton table has no task rows")
        for number, cells in rows[1:]:
            if len(cells) != 6:
                msg = "baton task needs six cells"
                if len(cells) > 6:
                    msg += r" (a literal | inside a cell is written \|)"
                self.error(page.path, number, msg)
                continue
            order, task, start, done, verification, _notes = cells
            activity = re.match(r"^(T[1-9]\d*)\s*-\s*\S", task)
            if activity and open_ids is not None and activity[1] not in open_ids \
                    and self.tracker_ids is not None and activity[1] in self.tracker_ids:
                self.info("handoff-baton-id-closed",
                          f"baton task {activity[1]} is closed in the tracker; refresh the handoff with /wiki-sync",
                          page.path, number)
            elif not activity or (open_ids is not None and activity[1] not in open_ids):
                self.error(page.path, number, "baton task must start with an open tracker ID (T1 - task)")
            if not re.fullmatch(r"[1-9]\d*", order):
                self.error(page.path, number, "baton order must be a positive integer")
            for name, value in (("start files", start), ("done criteria", done), ("verification command", verification)):
                if unresolved(value) or (name == "verification command" and value.lower().startswith("not verified") and (not value.lower().startswith("not verified - ") or unresolved(value[15:]))):
                    self.error(page.path, number, f"baton task missing {name}")

    def run(self):
        try:
            schema = self.read_page(self.wiki / "SCHEMA.md")
        except (OSError, UnicodeError) as exc:
            raise ValueError(f"cannot read SCHEMA.md ({type(exc).__name__})") from exc
        paths = self.core_map(schema)
        exclusions = self.excluded(schema, paths)
        self.page_types(schema)
        skipped = 0
        # rglob does not follow directory symlinks. A safe adopted Core path
        # still needs its role-specific validation even when reached via one.
        for path in paths.values():
            if path.is_file() and path not in self.pages:
                self.load(path)
        for path in sorted(self.wiki.rglob("*.md")):
            # Never read symlink targets outside the wiki or confidential term files.
            if private_terms_path(path):
                continue
            if not path.resolve().is_relative_to(self.wiki):
                self.error(path, 1, "wiki page points outside the wiki")
                continue
            if path not in self.pages and any(fnmatch.fnmatchcase(path.relative_to(self.wiki).as_posix(), g) for g in exclusions):
                skipped += 1
                continue
            if path not in self.pages:
                self.load(path)
        if skipped:
            self.info("paths-excluded", f"{skipped} paths excluded by SCHEMA")
        for page in self.pages.values():
            self.frontmatter(page)
            self.links(page)
        context = self.pages.get(paths.get("context"))
        if context:
            for marker, heading in CONTEXT.items():
                self.section(context, marker, heading)
        tracker = self.pages.get(paths.get("tracker"))
        open_ids = self.tracker(tracker) if tracker else None
        handoff = self.pages.get(paths.get("handoff"))
        if handoff:
            self.handoff(handoff, open_ids)
        if tracker:
            self.next_steps(tracker)
        for role, check in (("index", self.owners), ("risks", self.risk_register)):
            page = self.pages.get(paths.get(role))
            if page:
                check(page)
        has_core_map = any(l.strip() in ("## Core map", "<!-- wiki:core-map -->") for l in schema.lines)
        self.format_upgrades(schema, paths, has_core_map)
        return self.findings


def main(argv: list[str]) -> int:
    if argv[1:] == ["--version"]:
        print(f"validate-wiki {VERSION} (format {FORMAT_VERSION})")
        return 0
    args = argv[1:]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]

    def stop(message: str) -> int:
        if as_json:
            print(json.dumps({"validator": VERSION, "format": FORMAT_VERSION, "wiki": None, "exit": 2,
                              "error": message, "findings": [], "upgrades": [], "infos": []}, ensure_ascii=False))
        print(message, file=sys.stderr)
        return 2

    if sys.version_info < (3, 10):
        return stop("validate-wiki.py requires Python 3.10+; deterministic validation not run")
    if len(args) != 1 or args[0].startswith("-"):
        return stop("usage: python3 <maintainer>/scripts/validate-wiki.py [--json] <wiki-root>")
    wiki = Path(args[0])
    if not wiki.is_dir() or not (wiki / "SCHEMA.md").is_file() or private_terms_path(wiki / "SCHEMA.md") or not (wiki / "SCHEMA.md").resolve().is_relative_to(wiki.resolve()):
        return stop("configuration error: wiki-root needs a readable SCHEMA.md inside it")
    try:
        validator = Validator(wiki)
        validator.run()
    except ValueError as exc:
        return stop(f"configuration error: {exc}")
    except (OSError, UnicodeError) as exc:
        return stop(f"configuration error: cannot read documented wiki format ({type(exc).__name__})")
    code = 1 if validator.findings else 0
    if as_json:
        print(json.dumps(validator.report(code), ensure_ascii=False))
        return code
    for note in validator.infos:
        print("info: " + (f"{note.path}:{note.line}: " if note.path else "") + note.message)
    # `upgrade:` lines name what the current format still needs; they never change the exit code.
    for note in validator.upgrades:
        fix = f"; run /wiki-init --adopt {validator.root()} with plugin {VERSION}" if note.fix == "adopt" else ""
        print(f"upgrade: {note.path}:{note.line}: {note.message}{fix}")
    if code:
        print("\n".join(f"{n.path}:{n.line}: {n.message}" for n in validator.findings), file=sys.stderr)
        return 1
    print("wiki structural validation passed (semantic claims not checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
