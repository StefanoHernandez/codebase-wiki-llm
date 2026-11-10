#!/usr/bin/env python3
"""Behavioral fixtures for the installed, read-only wiki validator."""
from __future__ import annotations

import re
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


def adoption_cases():
    """Exercise pre-existing docs, not just current templates at adopted paths."""
    failures = 0
    for name in (
        "missing metadata reported once per page",
        "missing metadata still checks links",
        "unterminated metadata reported once",
        "empty metadata remains invalid",
        "archive reserved but absent",
        "archive nested reservation",
        "archive path is a file",
        "archive parent is a file",
        "archive dangling symlink",
        "archive dangling ancestor symlink",
        "archive symlink leaves wiki",
        "unreadable Open tracker suppresses dependent ID findings",
        "malformed Open tracker suppresses dependent ID findings",
        "unreadable Done tracker still checks Open references",
        "unreadable Open tracker still checks baton fields",
        "combined legacy adoption",
    ):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            wiki, roles = fixture(repo, localized=True)
            count = None
            required = []
            forbidden = []
            expected = 1
            if name.startswith("missing metadata") or name == "combined legacy adoption":
                for number in range(47):
                    (wiki / f"existing-{number}.md").write_text("# Existing documentation\n")
                count = 47
                required = ["frontmatter"]
                forbidden = ["missing frontmatter field", "confidence must", "sources must"]
                if name.endswith("checks links"):
                    (wiki / "existing-0.md").write_text("# Existing\n[missing](absent.md)\n")
                    count = 48
                    required.append("relative Markdown link")
            if name == "unterminated metadata reported once":
                (wiki / "existing.md").write_text("---\ntitle: Old page\n# Existing\n")
                count = 1
                required = ["unterminated frontmatter"]
            if name == "empty metadata remains invalid":
                (wiki / "existing.md").write_text("---\n---\n# Existing\n")
                required = ["missing frontmatter field title"]
            if name.startswith("archive") or name == "combined legacy adoption":
                archive = wiki / roles["log-archive"]
                archive.rmdir()
                expected = 0
                if name == "archive nested reservation":
                    schema = wiki / "SCHEMA.md"
                    schema.write_text(schema.read_text().replace(f"`{roles['log-archive']}`", "`future/nested/archive/`"))
                elif name == "archive path is a file":
                    archive.write_text("A file cannot become an archive directory.\n")
                    expected = 1
                elif name == "archive parent is a file":
                    blocked = wiki / "blocked"
                    blocked.write_text("file\n")
                    schema = wiki / "SCHEMA.md"
                    schema.write_text(schema.read_text().replace(f"`{roles['log-archive']}`", "`blocked/archive/`"))
                    expected = 1
                elif name == "archive dangling symlink":
                    archive.symlink_to(wiki / "absent-directory", target_is_directory=True)
                    expected = 1
                elif name == "archive dangling ancestor symlink":
                    (wiki / "dangling").symlink_to(wiki / "absent-directory", target_is_directory=True)
                    schema = wiki / "SCHEMA.md"
                    schema.write_text(schema.read_text().replace(f"`{roles['log-archive']}`", "`dangling/archive/`"))
                    expected = 1
                elif name == "archive symlink leaves wiki":
                    outside = repo / "outside"
                    outside.mkdir()
                    archive.symlink_to(outside, target_is_directory=True)
                    expected = 1
                if expected == 1:
                    required = ["Core map"]
                else:
                    count = 0
            if "tracker" in name or name == "combined legacy adoption":
                expected = 1
                tracker = wiki / roles["tracker"]
                # Localized fixture uses stable markers and positional columns.
                text = tracker.read_text()
                lines = text.splitlines()
                open_marker = lines.index("<!-- wiki:open -->")
                old_header = lines[open_marker + 1]
                old_delimiter = lines[open_marker + 2]
                old_row = lines[open_marker + 3]
                if "Done tracker" in name:
                    done_marker = lines.index("<!-- wiki:done -->")
                    text = text.replace("\n" + lines[done_marker + 1] + "\n", "\n| ID | Goal | Closed | Evidence |\n")
                    text = text.replace("\n" + lines[done_marker + 2] + "\n", "\n| --- | --- | --- | --- |\n", 1)
                elif "malformed Open" in name:
                    text = text.replace(old_delimiter, "| --- | --- | --- | --- | --- | --- | text |")
                else:
                    text = text.replace(old_header, "| ID | Status | Goal | Owner | Evidence |")
                    text = text.replace(old_delimiter, "| --- | --- | --- | --- | --- |", 1)
                    text = text.replace(old_row, "| T1 | 🟡 | Fix parser | Stefano | reproduced locally |")
                if name == "combined legacy adoption":
                    done_header = lines[lines.index("<!-- wiki:done -->") + 1]
                    text = text.replace("\n" + done_header + "\n", "\n| ID | Goal | Closed | Evidence |\n")
                    text = text.replace("<!-- wiki:done -->\n| ID | Goal | Closed | Evidence |\n" + lines[lines.index("<!-- wiki:done -->") + 2],
                                        "<!-- wiki:done -->\n| ID | Goal | Closed | Evidence |\n| --- | --- | --- | --- |")
                tracker.write_text(text)
                handoff = wiki / roles["handoff"]
                # Five legitimate tasks expose the old cascade from an unreadable Open table.
                text = handoff.read_text()
                task_row = next(line for line in text.splitlines() if line.startswith("| 1 | T1"))
                text = text.replace(task_row, "\n".join(task_row.replace("| 1 |", f"| {n} |", 1) for n in range(1, 6)))
                if "Done tracker" in name:
                    text = text.replace("T1 - Fix parser", "T99 - Missing task")
                    required = ["unsupported done tracker columns", "open tracker ID"]
                    forbidden = ["references not checked"]
                    count = 6
                else:
                    required = ["references not checked"]
                    forbidden = ["baton task must start with an open tracker ID"]
                    count = 2
                if "baton fields" in name:
                    text = text.replace("| `python3 -m unittest` |", "| |")
                    count = 7
                    required.append("missing verification command")
                handoff.write_text(text)
                if name == "combined legacy adoption":
                    count = 50  # 47 metadata gaps, 2 tracker layouts, 1 skipped reference check.
                    required += ["unsupported open tracker columns", "unsupported done tracker columns"]
                    forbidden += ["Core map log-archive", "missing frontmatter field"]
            before = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
            before_nodes = {p.relative_to(repo): (p.is_dir(), p.is_symlink()) for p in repo.rglob("*")}
            result = subprocess.run([sys.executable, "-I", str(VALIDATOR), str(wiki)], cwd=repo, capture_output=True, text=True)
            output = result.stdout + result.stderr
            findings = result.stderr.splitlines()
            after = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
            after_nodes = {p.relative_to(repo): (p.is_dir(), p.is_symlink()) for p in repo.rglob("*")}
            ok = (result.returncode == expected and (count is None or len(findings) == count)
                  and all(term in output for term in required) and all(term not in output for term in forbidden)
                  and before == after and before_nodes == after_nodes)
            print(("PASS " if ok else "FAIL ") + name)
            if not ok:
                failures += 1
                print(f"  expected exit {expected}, findings {count}; got {result.returncode}, {len(findings)}: {output.strip()}")
    return failures


EXCL = "\n## Excluded paths\n\n- `results/*-data/**`\n"
REPORT = "results/run-data/report-1.md"
TYPES = "\n## Page types\n\n| Path | type |\n| --- | --- |\n| `project/*` | `Project` |\n"


def schema_section_cases():
    """Optional SCHEMA sections: Excluded paths and Page types."""
    failures = 0
    # name, SCHEMA suffix, create REPORT, index suffix, exit, required, forbidden
    cases = [
        ("excluded report skipped", EXCL, True, "", 0, ["1 paths excluded"], []),
        ("report without exclusion", "", True, "", 1, ["missing or unterminated frontmatter"], []),
        ("link into excluded file", EXCL, True, f"[r]({REPORT})\n", 0, ["1 paths excluded"], ["link"]),
        ("exclusion cannot hide Core map", "\n## Excluded paths\n\n- `**`\n", False, "", 1,
         ["Excluded paths must not match SCHEMA or Core map pages"], []),
        ("unsafe exclusion glob", "\n## Excluded paths\n\n- `../x/*`\n", False, "", 1, ["unsafe Excluded paths glob"], []),
        ("malformed exclusion bullet", "\n## Excluded paths\n\n- results/*\n", False, "", 1, ["Excluded paths entry"], []),
        ("excluded paths prose ignored", "\n## Excluded paths\n\nGenerated data, not pages.\n\n- `results/*-data/**`\n",
         True, "", 0, ["1 paths excluded"], []),
        ("no section, no info", "", False, "", 0, [], ["excluded"]),
        ("valid page types", TYPES, False, "", 0, ["validation passed"], []),
        ("page types wrong header", TYPES.replace("| Path | type |", "| Glob | Kind |"), False, "", 1, ["Page types table"], []),
        ("page types one cell", TYPES + "| `adr/*` |\n", False, "", 1, ["Page types row"], []),
        ("page types unsafe glob", TYPES + "| `../x/*` | `X` |\n", False, "", 1, ["unsafe Page types glob"], []),
        ("page types empty type", TYPES + "| `adr/*` |  |\n", False, "", 1, ["Page types row"], []),
    ]
    for name, schema_suffix, report, index_suffix, expected, required, forbidden in cases:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            wiki, roles = fixture(repo)
            schema = wiki / "SCHEMA.md"
            schema.write_text(schema.read_text() + schema_suffix)
            if report:
                (wiki / REPORT).parent.mkdir(parents=True)
                (wiki / REPORT).write_text("# no frontmatter\n")
            index = wiki / roles["index"]
            index.write_text(index.read_text() + index_suffix)
            result = subprocess.run([sys.executable, "-I", str(VALIDATOR), str(wiki)], cwd=repo, capture_output=True, text=True)
            output = result.stdout + result.stderr
            ok = (result.returncode == expected and all(term in output for term in required)
                  and all(term not in output for term in forbidden))
            print(("PASS " if ok else "FAIL ") + name)
            if not ok:
                failures += 1
                print(f"  expected exit {expected}; got {result.returncode}: {output.strip()}")
    return failures


CURRENT_VERSION = (ROOT / "canonical/codebase/VERSION").read_text().strip()
SCHEMA_SECTIONS = ["Project profile", "Conventions", "Evidence", "Confidentiality", "Budgets",
                   "Log format", "Topics", "Page frontmatter"]


def current_schema(wiki, version=CURRENT_VERSION, drop=()):
    """Bring the fixture SCHEMA to the current format: version plus every v2 section."""
    schema = wiki / "SCHEMA.md"
    text = schema.read_text()
    if version is not None:
        text = text.replace("title: Schema\n", f"title: Schema\nformat_version: {version}\n", 1)
    text += "".join(f"\n## {name}\n\nText.\n" for name in SCHEMA_SECTIONS if name not in drop)
    schema.write_text(text)


DECISION = "---\ntitle: 0001 - Use X\nupdated: 2026-10-01\nsources:\n  - src/main.py\nsource_commit: abc123\nconfidence: high\n{status}---\n\n# 0001 - Use X\n\n## Decision\nUse X.\n{approval}"


def validate(repo, wiki):
    result = subprocess.run([sys.executable, "-I", str(VALIDATOR), str(wiki)], cwd=repo, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def write_decision(status, approval, body_status=False):
    def setup(w, r):
        current_schema(w)
        text = DECISION.format(status=status, approval=approval)
        if body_status:
            text = text.replace("## Decision", "- **Status**: accepted\n\n## Decision")
        (w / r["decisions"] / "0001-use-x.md").write_text(text)
    return setup


def legacy_done(w, r):
    current_schema(w)
    tracker = w / r["tracker"]
    tracker.write_text(tracker.read_text().replace(
        "| ID | Status | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- | --- |",
        "| ID | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- |"))


def translated_budgets(w, r):
    current_schema(w, drop=("Budgets",))
    schema = w / "SCHEMA.md"
    schema.write_text(schema.read_text() + "\n## Limiti\n<!-- wiki:budgets -->\n\nTesto.\n")


def upgrade_cases():
    """Format version and the `upgrade:` lines: stdout only, exit code unchanged."""
    failures = 0
    newer = ".".join(str(int(p) + 1) if i == 0 else p for i, p in enumerate(CURRENT_VERSION.split(".")))
    approval = "\n## Approval\naccepted: Stefano, meeting, 2026-10-01\n"
    translated = "\n## Approvazione\n<!-- wiki:approval -->\nproposta da Stefano, 2026-10-01\n"
    # name, setup(wiki, roles), legacy fixture, required upgrade texts (empty = no upgrade lines)
    cases = [
        ("current format has no upgrade lines", lambda w, r: current_schema(w), False, []),
        ("format_version missing", lambda w, r: current_schema(w, version=None), False, ["format_version missing"]),
        ("format_version older", lambda w, r: current_schema(w, version="0.11.0"), False, ["is older than " + CURRENT_VERSION]),
        ("format_version compared numerically", lambda w, r: current_schema(w, version="0.9.2"), False, ["is older than"]),
        ("format_version newer", lambda w, r: current_schema(w, version=newer), False, ["update the plugin"]),
        ("schema section missing", lambda w, r: current_schema(w, drop=("Page frontmatter",)), False, ["Page frontmatter"]),
        ("translated schema section by marker", translated_budgets, False, []),
        ("decision status in body only", write_decision("", approval, body_status=True), False, ["status must be in frontmatter"]),
        ("decision status out of format", write_decision("status: Accepted\n", approval), False, ["decision status must be"]),
        ("decision without approval", write_decision("status: accepted\n", ""), False, ["no ## Approval section"]),
        ("decision complete", write_decision("status: superseded by 0002\n", approval), False, []),
        ("translated approval by marker", write_decision("status: proposed\n", translated), False, []),
        ("legacy Done table without Status", legacy_done, False, ["Done table has no Status column"]),
        ("v1 wiki without Core map", lambda w, r: current_schema(w), True, ["Core map missing", "decisions must be a folder"]),
    ]
    cases += [
        ("format_version not X.Y.Z", lambda w, r: current_schema(w, version="0.12"), False, ["must be X.Y.Z"]),
        ("format_version prerelease", lambda w, r: current_schema(w, version="1.0.0-rc"), False, ["must be X.Y.Z"]),
        # A newer wiki must not get adopt suggestions from an older plugin.
        ("newer format proposes nothing else", lambda w, r: current_schema(w, version=newer, drop=("Budgets",)), False,
         ["update the plugin", "!Budgets", "!run /wiki-init"]),
        ("decision outside NNNN- naming skipped", lambda w, r: (current_schema(w), (w / r["decisions"] / "README.md").write_text(DECISION.format(status="", approval=""))), False, []),
    ]
    for name, setup, legacy, required in cases:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            wiki, roles = fixture(repo, legacy=legacy)
            setup(wiki, roles)
            code, out, err = validate(repo, wiki)
            upgrades = [line for line in out.splitlines() if line.startswith("upgrade:")]
            wanted = [t for t in required if not t.startswith("!")]
            ok = code == 0 and all(any(t in u for u in upgrades) for t in wanted) and (bool(wanted) or not upgrades)
            ok = ok and not any(t[1:] in u for t in required if t.startswith("!") for u in upgrades)
            ok = ok and all(re.match(r"upgrade: .+\.md:\d+: ", u) for u in upgrades)
            # Tools parse the fix: real wiki path, never the placeholder.
            ok = ok and all("<wiki-root>" not in u for u in upgrades)
            ok = ok and all(u.endswith("update the plugin") or u.endswith(f"run /wiki-init --adopt {wiki.relative_to(repo)} with plugin {CURRENT_VERSION}") for u in upgrades)
            print(("PASS " if ok else "FAIL ") + name)
            if not ok:
                failures += 1
                print(f"  expected exit 0, upgrades {required}; got {code}: {(out + err).strip()}")
    return failures


def versal_scenario():
    """Spec test 9: a 0.11.0 wiki shaped like Versal reaches zero upgrade lines after the adopt edits."""
    with tempfile.TemporaryDirectory() as temp:
        repo = Path(temp)
        wiki, roles = fixture(repo)
        current_schema(wiki, version=None, drop=("Page frontmatter",))
        tracker = wiki / roles["tracker"]
        tracker.write_text(tracker.read_text().replace(
            "| ID | Status | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- | --- |",
            "| ID | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- |"))
        schema = wiki / "SCHEMA.md"
        decision = wiki / roles["decisions"] / "0001-use-x.md"
        decision.write_text(DECISION.format(status="", approval="").replace("## Decision", "- **Status**: accepted\n\n## Decision"))
        code, out, _ = validate(repo, wiki)
        before = [u for u in out.splitlines() if u.startswith("upgrade:")]
        texts = ["format_version missing", "Page frontmatter", "Done table has no Status", "status must be in frontmatter", "no ## Approval"]
        ok = code == 0 and len(before) == len(texts) and all(any(t in u for u in before) for t in texts)
        # The adopt edits of wiki-init Step 4, layout unchanged.
        tracker = wiki / roles["tracker"]
        tracker.write_text(tracker.read_text().replace(
            "| ID | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- |",
            "| ID | Status | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- | --- |"))
        lines = tracker.read_text().split("\n")
        done = lines.index("| ID | Status | Goal | Closed | Criteria met | Evidence |")
        for i in range(done + 2, len(lines)):
            if not lines[i].startswith("| "):
                break
            cells = lines[i].split("|")
            lines[i] = "|".join(cells[:2] + [" 🟢 "] + cells[2:])
        tracker.write_text("\n".join(lines))
        decision.write_text(decision.read_text().replace("confidence: high\n", "confidence: high\nstatus: accepted\n", 1) + "\n## Approval\nApproval not recorded.\n")
        schema.write_text(schema.read_text().replace("title: Schema\n", f"title: Schema\nformat_version: {CURRENT_VERSION}\n", 1) + "\n## Page frontmatter\n\nText.\n")
        code_after, out_after, err_after = validate(repo, wiki)
        ok = ok and code_after == 0 and "upgrade:" not in out_after
        print(("PASS " if ok else "FAIL ") + "Versal-shaped wiki upgraded to zero upgrade lines")
        if not ok:
            print(f"  before {code}: {before}\n  after {code_after}: {(out_after + err_after).strip()}")
        return 0 if ok else 1


def upgrade_with_findings():
    """Upgrade lines go to stdout beside findings; the exit code comes from the findings."""
    with tempfile.TemporaryDirectory() as temp:
        repo = Path(temp)
        wiki, roles = fixture(repo)
        current_schema(wiki, version=None)
        index = wiki / roles["index"]
        index.write_text(index.read_text().replace("src/main.py", "src/missing.py"))
        code, out, err = validate(repo, wiki)
        ok = code == 1 and "format_version missing" in out and "source" in err
        print(("PASS " if ok else "FAIL ") + "upgrade lines with findings exit 1")
        if not ok:
            print(f"  got {code}: {(out + err).strip()}")
        return 0 if ok else 1


OWNERS = "\n## How this wiki is organised\n<!-- wiki:owners -->\n\n| Topic | Owner page |\n| --- | --- |\n| Status | [tracker](project/work-tracker.md) |\n"
NEXT = "## Next steps\n<!-- wiki:next -->\n\n**In one line:** parser fix in progress.\n\n1. Fix the parser ({id})\n\n"
RISKS = "\n## Register\n<!-- wiki:risk-register -->\n\n| ID | Risk | Severity | Trigger | Mitigation | Owner | IDs |\n| --- | --- | --- | --- | --- | --- | --- |\n{rows}"
RISK = "| {id} | Parser breaks | {sev} | new input format | fixtures | Stefano | {ids} |\n"


def append_to(role, text):
    def setup(w, r):
        page = w / r[role]
        page.write_text(page.read_text() + text)
    return setup


def next_steps(ident):
    def setup(w, r):
        tracker = w / r["tracker"]
        tracker.write_text(tracker.read_text().replace("## Open\n", NEXT.format(id=ident) + "## Open\n", 1))
    return setup


def done_row(w, r):
    tracker = w / r["tracker"]
    header = "| ID | Status | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- | --- |\n"
    tracker.write_text(tracker.read_text().replace(header, header + "| T7 | 🟢 | short |\n", 1))


def marker_cases():
    """Optional sections: owners table, next steps, risk register."""
    failures = 0
    bad_header = OWNERS.replace("| Topic | Owner page |\n| --- | --- |", "| A | B | C |\n| --- | --- | --- |")
    # name, setup, expected exit, required finding text
    cases = [
        ("owners table valid", append_to("index", OWNERS), 0, ""),
        ("owners table wrong header", append_to("index", bad_header), 1, "owners table"),
        ("owners row without link", append_to("index", OWNERS + "| Dates | schedule |\n"), 1, "owner page link"),
        ("next steps cite existing ID", next_steps("T1"), 0, ""),
        ("next steps cite unknown ID", next_steps("T99"), 1, "Next steps cites unknown tracker ID T99"),
        ("risk register valid", append_to("risks", RISKS.format(rows=RISK.format(id="R1", sev="high", ids="T1"))), 0, ""),
        ("risk register duplicate ID", append_to("risks", RISKS.format(rows=RISK.format(id="R1", sev="high", ids="T1") * 2)), 1, "duplicate risk ID R1"),
        ("risk register bad ID", append_to("risks", RISKS.format(rows=RISK.format(id="X1", sev="high", ids="T1"))), 1, "risk ID must be R"),
        ("risk register unknown severity", append_to("risks", RISKS.format(rows=RISK.format(id="R1", sev="huge", ids="T1"))), 1, "risk severity must be"),
        ("risk register reordered English header", append_to("risks", RISKS.replace("| ID | Risk | Severity |", "| ID | Severity | Risk |").format(rows=RISK.format(id="R1", sev="high", ids="T1"))), 1, "unsupported risk register"),
        ("risk severity is a fixed lowercase token", append_to("risks", RISKS.format(rows=RISK.format(id="R1", sev="High", ids="T1"))), 1, "risk severity must be"),
        ("owners partial English header", append_to("index", OWNERS.replace("| Topic | Owner page |", "| Topic | Page |")), 1, "owners table"),
        ("unreadable Done row stops ID checks", lambda w, r: (done_row(w, r), append_to("risks", RISKS.format(rows=RISK.format(id="R1", sev="low", ids="T7")))(w, r)), 1, "risk tracker references not checked"),
        ("risk register unknown tracker ID", append_to("risks", RISKS.format(rows=RISK.format(id="R1", sev="low", ids="T99"))), 1, "risk cites unknown tracker ID T99"),
    ]
    for name, setup, expected, required in cases:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            wiki, roles = fixture(repo)
            current_schema(wiki)
            setup(wiki, roles)
            code, out, err = validate(repo, wiki)
            ok = code == expected and required in err and "upgrade:" not in out
            print(("PASS " if ok else "FAIL ") + name)
            if not ok:
                failures += 1
                print(f"  expected exit {expected}, {required!r}; got {code}: {(out + err).strip()}")
    return failures


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
        ("balanced parenthesized inline link", ("index", "# Page", '[Guide](guide(v2).md "Guide title")'), 0, ""),
        ("nested parenthesized inline link", ("index", "# Page", "[Guide](guide(v(2)).md#anchor 'Guide title')"), 0, ""),
        ("escaped parenthesized inline link", ("index", "# Page", r"[Guide](guide\(v2\).md)"), 0, ""),
        ("escaped unmatched parenthesis inline link", ("index", "# Page", r"[Guide](guide\)v2.md)"), 0, ""),
        ("angle inline link with spaces and title", ("index", "# Page", '[Guide](<guide (v2).md> "Guide title")'), 0, ""),
        ("angle inline link with escaped parentheses", ("index", "# Page", r"[Guide](<guide\(v2\).md> 'Guide title')"), 0, ""),
        ("broken parenthesized inline link", ("index", "# Page", '[Guide](missing(v2).md "Guide title")'), 1, "link"),
        ("broken escaped parenthesized inline link", ("index", "# Page", r"[Guide](missing\(v2\).md)"), 1, "link"),
        ("code and external links ignored", ("index", "# Page", "[web](https://example.org/no.md) [mail](mailto:a@example.org)\n```md\n[missing](no.md)\n<!-- wiki:baton -->\n```\n`[inline](missing.md)`\n[anchor](#absent)"), 0, ""),
        ("unsafe Core path", ("SCHEMA", "`index.md`", "`../outside.md`"), 1, "Core map"),
        ("missing Core path", ("SCHEMA", "`index.md`", "`absent.md`"), 1, "Core map"),
        ("adopted decisions file retained", ("SCHEMA", "`project/decisions/`", "`project/decisions.md`"), 0, ""),
        ("adopted decisions file frontmatter checked", ("SCHEMA", "`project/decisions/`", "`project/decisions.md`"), 1, "updated"),
        ("missing Core role", ("SCHEMA", "| index | `index.md` |", ""), 1, "Core map"),
        ("duplicate Core role", ("SCHEMA", "| index | `index.md` |", "| index | `index.md` |\n| index | `log.md` |"), 1, "Core map"),
        ("duplicate tracker ID", ("tracker", TRACKER, TRACKER + GREEN.replace("T2", "T1")), 1, "duplicate"),
        ("IDs elsewhere are references", ("index", "# Page", "T1, T1; see T1"), 0, ""),
        ("translated heading without marker", ("context", "## Read First\n<!-- wiki:read-first -->", "## Leggi prima"), 1, "wiki:read-first"),
        ("mapped internal directory symlink", ("context", "## Read First\n<!-- wiki:read-first -->", "## Leggi prima"), 1, "wiki:read-first"),
        ("missing handoff state marker", ("handoff", "## Current Work State\n<!-- wiki:state -->", "## Stato"), 1, "wiki:state"),
        ("no-work with open tracker", ("handoff", HANDOFF.split("## Baton For Next Coding Agent\n<!-- wiki:baton -->\n")[1].split("## Blockers")[0], "No open work.\n"), 1, "open"),
        ("no-work open row without leading pipe", None, 1, "contradicts open tracker"),
        ("no-work open row without trailing pipe", None, 1, "contradicts open tracker"),
        ("no-work open row without outer pipes", None, 1, "contradicts open tracker"),
        ("duplicate ID row without leading pipe", ("tracker", TRACKER, TRACKER + GREEN.replace("T2", "T1").lstrip("|")), 1, "duplicate"),
        ("black closure without trailing pipe", ("tracker", TRACKER, TRACKER + GREEN.replace("🟢", "⚫").rstrip("\n|") + "\n"), 1, "closed by"),
        ("green unproven row without outer pipes", ("tracker", TRACKER, TRACKER + BLACK.replace("⚫", "🟢").strip("\n|") + "\n"), 1, "unproven"),
        ("healthy tables without outer pipes", None, 0, ""),
        ("pipeline prose before Open table", ("tracker", "<!-- wiki:open -->\n", "<!-- wiki:open -->\n\nVerification uses `printf x | cat`.\n\n"), 0, ""),
        ("pipeline prose after Open table", ("tracker", "## Proposals", "\nVerification uses `printf x | cat`.\n\n## Proposals"), 0, ""),
        ("pipeline prose around tables", None, 0, ""),
        ("pipeline prose around localized tables", None, 0, ""),
        ("pipeline prose around legacy tables", None, 0, ""),
        ("pipeline prose around tables without outer pipes", None, 0, ""),
        ("unsupported contiguous tracker row", ("tracker", TRACKER.splitlines()[4], "T1 unsupported row"), 1, "table row"),
        ("escaped pipe table commands", None, 0, ""),
        ("missing baton verification", ("handoff", "| `python3 -m unittest` | none |", "| Not verified - | none |"), 1, "verification"),
        ("reordered baton header", ("handoff", "| Order | Task | Start files", "| Task | Order | Start files"), 1, "baton"),
        ("baton missing delimiter", ("handoff", "| --- | --- | --- | --- | --- | --- |\n", ""), 1, "delimiter"),
        ("baton malformed delimiter", ("handoff", "| --- | --- | --- | --- | --- | --- |", "| --- | --- | --- | --- | --- | text |"), 1, "delimiter"),
        ("Core map missing delimiter", ("SCHEMA", "| --- | --- |\n", ""), 1, "delimiter"),
        ("Core map delimiter width mismatch", ("SCHEMA", "| --- | --- |", "| --- | --- | --- |"), 1, "delimiter"),
        ("Open tracker missing delimiter", ("tracker", "| --- | --- | --- | --- | --- | --- | --- |\n", ""), 1, "delimiter"),
        ("Proposals tracker missing delimiter", ("tracker", "| Proposal | By | Date | Why |\n| --- | --- | --- | --- |\n", "| Proposal | By | Date | Why |\n"), 1, "delimiter"),
        ("Done tracker missing delimiter", ("tracker", "| ID | Status | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- | --- |\n", "| ID | Status | Goal | Closed | Criteria met | Evidence |\n"), 1, "delimiter"),
        ("empty source path", ("index", "src/main.py", "#symbol"), 1, "source"),
        ("black agent authority", ("tracker", TRACKER, TRACKER + BLACK.replace("closed by Stefano", "closed by agent")), 1, "human"),
        ("green explicit not verified", ("tracker", TRACKER, TRACKER + GREEN.replace("Review passed", "⚠️ NOT VERIFIED - review not run")), 1, "unproven"),
        ("green evidence explicitly not verified", ("tracker", TRACKER, TRACKER + GREEN.replace("recorded review", "⚠️ NOT VERIFIED - review never ran")), 1, "unproven"),
        ("green evidence negative plain marker", ("tracker", TRACKER, TRACKER + GREEN.replace("recorded review", "Not verified - review never ran")), 1, "unproven"),
        ("green evidence negative marker without reason", ("tracker", TRACKER, TRACKER + GREEN.replace("recorded review", "⚠️ NOT VERIFIED")), 1, "unproven"),
        ("green evidence human unproven closure", ("tracker", TRACKER, TRACKER + GREEN.replace("recorded review", "closed by Stefano 2026-10-01; not proven: cancelled")), 1, "unproven"),
        ("green descriptive unproven scenarios", ("tracker", TRACKER, TRACKER + GREEN.replace("Review passed", "Review passed for unproven closure scenarios").replace("recorded review", "Tests document not verified scenarios")), 0, ""),
        ("green quoted negative marker", ("tracker", TRACKER, TRACKER + GREEN.replace("Review passed", 'Review of "NOT VERIFIED - offline" behavior passed').replace("recorded review", 'Documented "⚠️ NOT VERIFIED - offline" examples')), 0, ""),
        ("explicit unavailable verification", ("handoff", "| `python3 -m unittest` | none |", "| Not verified - server unavailable | none |"), 0, ""),
        ("baton missing ID", ("handoff", "T1 - Fix parser", "Fix parser"), 1, "tracker ID"),
        ("green closure", ("tracker", TRACKER, TRACKER + GREEN), 0, ""),
        ("black closure", ("tracker", TRACKER, TRACKER + BLACK), 0, ""),
        ("green unproven closure", ("tracker", TRACKER, TRACKER + BLACK.replace("⚫", "🟢")), 1, "unproven"),
        ("black without authority", ("tracker", TRACKER, TRACKER + GREEN.replace("🟢", "⚫")), 1, "closed by"),
        ("black missing evidence", ("tracker", TRACKER, TRACKER + BLACK.replace("conversation 2026-10-01", "")), 1, "evidence"),
        ("black invalid closure date", ("tracker", TRACKER, TRACKER + BLACK.replace("Stefano 2026-10-01", "Stefano 2026-02-30")), 1, "closure date"),
        ("legacy proven Done", ("tracker", TRACKER, TRACKER.replace("| ID | Status | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- | --- |", "| ID | Goal | Closed | Criteria met | Evidence |\n| --- | --- | --- | --- | --- |") + GREEN.replace("| 🟢 ", "")), 0, ""),
        ("proposal with ID", ("tracker", "## Done", "| T8 | Stefano | 2026-10-01 | idea |\n## Done"), 1, "proposal"),
        ("missing source_commit", ("index", "source_commit: abc123\n", ""), 1, "source_commit"),
        ("empty title", ("index", "title: index", "title: ''"), 1, "title"),
        ("unterminated double quoted title", ("index", "title: index", 'title: "index'), 1, "quote"),
        ("unterminated single quoted title", ("index", "title: index", "title: 'index"), 1, "quote"),
        ("escaped closing quote is unterminated", ("index", "title: index", 'title: "index\\"'), 1, "quote"),
        ("unterminated quoted source list", ("index", "  - src/main.py", '  - "src/main.py'), 1, "quote"),
        ("valid quoted scalar and source", ("index", "title: index\nupdated: 2026-10-01\nsources:\n  - src/main.py", 'title: "index"\nupdated: 2026-10-01\nsources:\n  - \'src/main.py\''), 0, ""),
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
            wiki, roles = fixture(repo, localized="localized" in name,
                                  legacy=name in ("legacy English fallback", "pipeline prose around legacy tables"))
            if mutation:
                role, old, new = mutation
                path = wiki / ("SCHEMA.md" if role == "SCHEMA" else roles[role])
                original = path.read_text()
                assert old in original, (name, old)
                path.write_text(original.replace(old, new))
            if name == "decoded page-relative link":
                (wiki / "space name.md").write_text(frontmatter() + "# Page\n")
            if "inline link" in name and not name.startswith("broken"):
                target = {"nested parenthesized inline link": "guide(v(2)).md",
                          "escaped unmatched parenthesis inline link": "guide)v2.md",
                          "angle inline link with spaces and title": "guide (v2).md"}.get(name, "guide(v2).md")
                (wiki / target).write_text(frontmatter() + "# Guide\n")
            if name.startswith("adopted decisions file"):
                page = frontmatter("Decisions") + "# Existing v1 decisions\n"
                if name.endswith("frontmatter checked"):
                    page = page.replace("2026-10-01", "2026-02-30")
                (wiki / "project/decisions.md").write_text(page)
            if name.startswith("no-work open row without"):
                row = TRACKER.splitlines()[4]
                if name.endswith("leading pipe") or name.endswith("outer pipes"):
                    row = row.lstrip("|")
                if name.endswith("trailing pipe") or name.endswith("outer pipes"):
                    row = row.rstrip("|")
                tracker = wiki / roles["tracker"]
                tracker.write_text(tracker.read_text().replace(TRACKER.splitlines()[4], row))
                handoff = wiki / roles["handoff"]
                old = HANDOFF.split("<!-- wiki:baton -->\n")[1].split("## Blockers")[0]
                handoff.write_text(handoff.read_text().replace(old, "No open work.\n"))
            if name == "healthy tables without outer pipes":
                for role in ("tracker", "handoff"):
                    page = wiki / roles[role]
                    page.write_text("\n".join(line.strip("|") if line.startswith("|") else line
                                              for line in page.read_text().splitlines()) + "\n")
            if name.startswith("pipeline prose around"):
                for role in ("SCHEMA", "tracker", "handoff"):
                    page = wiki / ("SCHEMA.md" if role == "SCHEMA" else roles[role])
                    lines = page.read_text().splitlines()
                    body = []
                    for i, line in enumerate(lines):
                        if line.startswith("|") and (not i or not lines[i - 1].startswith("|")):
                            body.extend(["", "Verification uses `printf x | cat`.", ""])
                        body.append(line.strip("|") if "without outer pipes" in name and line.startswith("|") else line)
                        if line.startswith("|") and (i + 1 == len(lines) or not lines[i + 1].startswith("|")):
                            body.extend(["", "Recorded output uses `printf x | cat`.", ""])
                    page.write_text("\n".join(body) + "\n")
            if name == "escaped pipe table commands":
                for role in ("tracker", "handoff"):
                    page = wiki / roles[role]
                    page.write_text(page.read_text().replace("`python3 -m unittest`", r"`printf x \| cat`"))
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
    failures += adoption_cases()
    failures += schema_section_cases()
    failures += upgrade_cases()
    failures += marker_cases()
    failures += versal_scenario()
    failures += upgrade_with_findings()
    return int(failures > 0)


if __name__ == "__main__":
    raise SystemExit(run())
