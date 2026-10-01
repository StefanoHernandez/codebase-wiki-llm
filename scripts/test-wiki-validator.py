#!/usr/bin/env python3
"""Behavioral fixtures for the installed, read-only wiki validator."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "canonical/codebase/scripts/validate-wiki.py"
ROLES = {
    "index": "index.md", "log": "log.md", "log-archive": "log/",
    "tracker": "project/work-tracker.md", "decisions": "project/decisions/",
    "risks": "project/risks.md", "context": "agent/context.md",
    "handoff": "agent/handoff.md", "troubleshooting": "troubleshooting.md",
    "glossary": "glossary.md",
}
CONTEXT = """## Goals And Non-Goals
<!-- wiki:goals -->
Test the app.
## Non-Negotiable Rules
<!-- wiki:rules -->
Keep API stable.
## Frequent Commands
<!-- wiki:commands -->
`python3 -m unittest`
## Verified Facts
<!-- wiki:verified-facts -->
Tests are local.
## Read First
<!-- wiki:read-first -->
Read source.
"""
HANDOFF = """## Current Work State
<!-- wiki:state -->
- Tracker IDs: T1
- Goal: Fix parser
- Last completed step: reproduced failure
- Current branch: `main`
- Last commit: `abc123`
- Worktree: clean
## Baton For Next Coding Agent
<!-- wiki:baton -->
| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
| 1 | T1 - Fix parser | `src/main.py` | see T1 | `python3 -m unittest` | none |
## Blockers
<!-- wiki:blockers -->
None.
## Known Risks
<!-- wiki:risks -->
None.
## Commands Already Run
<!-- wiki:commands-run -->
Tests reproduced issue.
## Do Not Redo
<!-- wiki:do-not-redo -->
Reproduction.
## Evidence Trail
<!-- wiki:evidence-trail -->
Source and tracker.
"""
TRACKER = """## Open
<!-- wiki:open -->
| ID | Status | Goal | Done when | Owner | Next verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | 🟡 | Fix parser | Unit tests pass | Stefano | `python3 -m unittest` | reproduced locally |
## Proposals
<!-- wiki:proposals -->
| Proposal | By | Date | Why |
| --- | --- | --- | --- |
## Done
<!-- wiki:done -->
| ID | Status | Goal | Closed | Criteria met | Evidence |
| --- | --- | --- | --- | --- | --- |
"""
GREEN = "| T2 | 🟢 | Fix docs | 2026-10-01 | Review passed | recorded review |\n"
BLACK = "| T2 | ⚫ | Old feature | 2026-10-01 | closed by Stefano 2026-10-01; not proven: cancelled | conversation 2026-10-01 |\n"


def frontmatter(title="Page", sources="  - src/main.py\n"):
    return f"---\ntitle: {title}\nupdated: 2026-10-01\nsources:\n{sources}source_commit: abc123\nconfidence: high\n---\n\n"


def fixture(repo, localized=False, legacy=False):
    (repo / ".git").mkdir()
    (repo / "src").mkdir()
    (repo / "src/main.py").write_text("print('hello')\n")
    wiki = repo / ("docs/kb" if localized else "wiki")
    wiki.mkdir(parents=True)
    roles = {k: "locale/" + v if localized else v for k, v in ROLES.items()}
    schema = "---\ntitle: Schema\nupdated: 2026-10-01\nconfidence: high\n---\n"
    if not legacy:
        schema += "\n## Core map\n\n| Role | Path |\n| --- | --- |\n"
        schema += "".join(f"| {k} | `{v}` |\n" for k, v in roles.items())
    else:
        roles["decisions"] = "project/decisions.md"
        roles["troubleshooting"] = "engineering/troubleshooting.md"
        roles.pop("log-archive")
    (wiki / "SCHEMA.md").write_text(schema)
    for role, rel in roles.items():
        path = wiki / rel
        if rel.endswith("/"):
            path.mkdir(parents=True)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        body = {"context": CONTEXT, "handoff": HANDOFF, "tracker": TRACKER}.get(role, "# Page\n")
        if localized:
            body = "\n".join("## Sezione italiana" if ln.startswith("## ") else ln for ln in body.splitlines()) + "\n"
            for header in ("| Order | Task | Start files | Done when | Verification command | Notes / blockers |",
                           "| ID | Status | Goal | Done when | Owner | Next verification | Evidence |",
                           "| ID | Status | Goal | Closed | Criteria met | Evidence |"):
                count = len(header.strip("|").split("|"))
                body = body.replace(header, "| " + " | ".join(f"Colonna {i}" for i in range(count)) + " |")
        if legacy:
            body = "\n".join(ln for ln in body.splitlines() if not ln.startswith("<!-- wiki:")) + "\n"
        path.write_text(frontmatter(role) + body)
    # These concrete template substitutions must work from any installed location.
    for role, refs in {"handoff": ["log", "tracker"], "tracker": ["log", "handoff"], "context": ["index"]}.items():
        path = wiki / roles[role]
        sources = "  - src/main.py\n  - " + (wiki / "SCHEMA.md").relative_to(repo).as_posix() + "\n"
        sources += "".join("  - " + (wiki / roles[r]).relative_to(repo).as_posix() + "\n" for r in refs)
        text = path.read_text().replace("sources:\n  - src/main.py\n", "sources:\n" + sources)
        path.write_text(text)
    return wiki, roles


def run():
    if not VALIDATOR.is_file():
        print(f"FAIL installed structural validation absent: {VALIDATOR}", file=sys.stderr)
        return 1
    failures = 0
    cases = [
        ("healthy default", None, 0, ""),
        ("healthy adopted localized", None, 0, ""),
        ("legacy English fallback", None, 0, ""),
        ("invalid date", ("index", "2026-10-01", "2026-02-30"), 1, "updated"),
        ("missing source", ("index", "src/main.py", "src/missing.py"), 1, "source"),
        ("source placeholder", ("index", "src/main.py", "<source-path>"), 1, "source"),
        ("directory and suffixed sources", ("index", "src/main.py", "./src/main.py:1#main\n  - src/"), 0, ""),
        ("broken relative link", ("index", "# Page", "[missing](no.md)"), 1, "link"),
        ("decoded page-relative link", ("context", "Read source.", "[ok](../space%20name.md#anchor)"), 0, ""),
        ("code and external links ignored", ("index", "# Page", "[web](https://example.org/no.md) [mail](mailto:a@example.org)\n```md\n[missing](no.md)\n<!-- wiki:baton -->\n```\n`[inline](missing.md)`\n[anchor](#absent)"), 0, ""),
        ("unsafe Core path", ("SCHEMA", "`index.md`", "`../outside.md`"), 1, "Core map"),
        ("missing Core path", ("SCHEMA", "`index.md`", "`absent.md`"), 1, "Core map"),
        ("missing Core role", ("SCHEMA", "| index | `index.md` |", ""), 1, "Core map"),
        ("duplicate Core role", ("SCHEMA", "| index | `index.md` |", "| index | `index.md` |\n| index | `log.md` |"), 1, "Core map"),
        ("duplicate tracker ID", ("tracker", TRACKER, TRACKER + GREEN.replace("T2", "T1")), 1, "duplicate"),
        ("IDs elsewhere are references", ("index", "# Page", "T1, T1; see T1"), 0, ""),
        ("translated heading without marker", ("context", "## Read First\n<!-- wiki:read-first -->", "## Leggi prima"), 1, "wiki:read-first"),
        ("mapped internal directory symlink", ("context", "## Read First\n<!-- wiki:read-first -->", "## Leggi prima"), 1, "wiki:read-first"),
        ("missing handoff state marker", ("handoff", "## Current Work State\n<!-- wiki:state -->", "## Stato"), 1, "wiki:state"),
        ("no-work with open tracker", ("handoff", HANDOFF.split("## Baton For Next Coding Agent\n<!-- wiki:baton -->\n")[1].split("## Blockers")[0], "No open work.\n"), 1, "open"),
        ("missing baton verification", ("handoff", "| `python3 -m unittest` | none |", "| Not verified - | none |"), 1, "verification"),
        ("reordered baton header", ("handoff", "| Order | Task | Start files", "| Task | Order | Start files"), 1, "baton"),
        ("empty source path", ("index", "src/main.py", "#symbol"), 1, "source"),
        ("black agent authority", ("tracker", TRACKER, TRACKER + BLACK.replace("closed by Stefano", "closed by agent")), 1, "human"),
        ("green explicit not verified", ("tracker", TRACKER, TRACKER + GREEN.replace("Review passed", "⚠️ NOT VERIFIED - review not run")), 1, "unproven"),
        ("explicit unavailable verification", ("handoff", "| `python3 -m unittest` | none |", "| Not verified - server unavailable | none |"), 0, ""),
        ("baton missing ID", ("handoff", "T1 - Fix parser", "Fix parser"), 1, "tracker ID"),
        ("green closure", ("tracker", TRACKER, TRACKER + GREEN), 0, ""),
        ("black closure", ("tracker", TRACKER, TRACKER + BLACK), 0, ""),
        ("green unproven closure", ("tracker", TRACKER, TRACKER + BLACK.replace("⚫", "🟢")), 1, "unproven"),
        ("black without authority", ("tracker", TRACKER, TRACKER + GREEN.replace("🟢", "⚫")), 1, "closed by"),
        ("black missing evidence", ("tracker", TRACKER, TRACKER + BLACK.replace("conversation 2026-10-01", "")), 1, "evidence"),
        ("black invalid closure date", ("tracker", TRACKER, TRACKER + BLACK.replace("Stefano 2026-10-01", "Stefano 2026-02-30")), 1, "closure date"),
        ("legacy proven Done", ("tracker", TRACKER, TRACKER.replace("| ID | Status | Goal | Closed", "| ID | Goal | Closed").replace("| --- | --- | --- | --- | --- | --- |\n", "| --- | --- | --- | --- | --- |\n") + GREEN.replace("| 🟢 ", "")), 0, ""),
        ("proposal with ID", ("tracker", "## Done", "| T8 | Stefano | 2026-10-01 | idea |\n## Done"), 1, "proposal"),
        ("missing source_commit", ("index", "source_commit: abc123\n", ""), 1, "source_commit"),
        ("empty title", ("index", "title: index", "title: ''"), 1, "title"),
        ("invalid confidence", ("index", "confidence: high", "confidence: certain"), 1, "confidence"),
        ("unsupported YAML", ("index", "sources:\n  - src/main.py", "sources: [src/main.py]"), 1, "sources"),
        ("unsupported block scalar", ("index", "title: index", "title: |"), 1, "unsupported"),
        ("unsupported flow mapping", ("index", "title: index", "title: {name: index}"), 1, "unsupported"),
        ("valid no-work", None, 0, ""),
        ("private terms never read", None, 0, ""),
    ]
    for name, mutation, expected, diagnostic in cases:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            wiki, roles = fixture(repo, localized="localized" in name, legacy=name == "legacy English fallback")
            if mutation:
                role, old, new = mutation
                path = wiki / ("SCHEMA.md" if role == "SCHEMA" else roles[role])
                original = path.read_text()
                assert old in original, (name, old)
                path.write_text(original.replace(old, new))
            if name == "decoded page-relative link":
                (wiki / "space name.md").write_text(frontmatter() + "# Page\n")
            if name == "mapped internal directory symlink":
                (wiki / "alias").symlink_to(wiki / "agent", target_is_directory=True)
                schema = wiki / "SCHEMA.md"
                schema.write_text(schema.read_text().replace("`agent/context.md`", "`alias/context.md`"))
            if name == "valid no-work":
                tracker = wiki / roles["tracker"]
                tracker.write_text(tracker.read_text().replace(TRACKER.splitlines()[4] + "\n", ""))
                handoff = wiki / roles["handoff"]
                old = HANDOFF.split("<!-- wiki:baton -->\n")[1].split("## Blockers")[0]
                handoff.write_text(handoff.read_text().replace(old, "No open work.\n"))
            if name == "private terms never read":
                (wiki / ".private-terms").write_bytes(b"\xffsecret\x00")
                (wiki / "private-alias.md").symlink_to(wiki / ".private-terms")
            before = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
            result = subprocess.run([sys.executable, "-I", str(VALIDATOR), str(wiki)], cwd=repo, capture_output=True, text=True)
            output = result.stdout + result.stderr
            after = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
            ok = result.returncode == expected and diagnostic.lower() in output.lower() and before == after
            if expected == 1:
                import re
                ok = ok and bool(re.search(r"\.md:\d+:", output))
            print(("PASS " if ok else "FAIL ") + name)
            if not ok:
                failures += 1
                print(f"  expected exit {expected}, diagnostic {diagnostic!r}; got {result.returncode}: {output.strip()}")
    with tempfile.TemporaryDirectory() as temp:
        for args in ([], [temp], [temp, temp]):
            result = subprocess.run([sys.executable, "-I", str(VALIDATOR), *args], capture_output=True, text=True)
            if result.returncode != 2:
                print(f"FAIL configuration exit 2: {args}: {result.returncode}")
                failures += 1
    return int(failures > 0)


if __name__ == "__main__":
    raise SystemExit(run())
