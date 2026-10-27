# 0.11.0 Field Feedback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A wiki can exclude non-page Markdown and map its own folders to `type` through SCHEMA, lint reports confirmations that no longer cover current sources, and sync stops churning `generated`.

**Architecture:** Two optional SCHEMA sections (`## Excluded paths`, `## Page types`) parsed by the existing validator with its `section()`/`table()` helpers; everything else is agent-workflow prose in `canonical/codebase/`. Packages under `plugins/` and `skills/` are regenerated, never edited.

**Tech Stack:** Python 3.10+ stdlib (`fnmatch`), Markdown workflows, bash test runners.

**Spec:** `docs/superpowers/specs/2026-10-27-okf-field-feedback-design.md`

## Global Constraints

- Python 3.10 floor: no `PurePath.full_match`; matching is `fnmatch.fnmatchcase(<wiki-relative POSIX path>, <glob>)`.
- Timestamps stay ISO 8601 datetimes with `Z` (OKF v0.2 `3dc3029`); no date-only option anywhere.
- Trust tiers are derived from `verified` only; staleness is a separate signal and never changes the tier.
- Agents never write or edit `verified`.
- Variant: codebase only. Secondbrain untouched.
- Edit `canonical/` and `scripts/` only; run `python3 scripts/generate-codebase-packages.py` to refresh `plugins/`, `skills/`, `.claude-plugin/`.
- Canonical Markdown must not contain a literal `wiki/` path (`scripts/check-generated.sh` greps for it); write `<wiki-root>/`.
- Validator stays read-only and git-free; info lines go to stdout and never change the exit code.
- Version 0.11.0 in `canonical/codebase/VERSION` and `.claude-plugin/marketplace.json`.
- Commits on `dev`, message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. A glob that matches every page (`**` or `*`) → must not silence the wiki: SCHEMA and Core map files still validated, error raised. Test: "exclusion cannot hide Core map".
2. Prose or an example code block under `## Excluded paths` / `## Page types` in a real SCHEMA → must not be parsed as rules; only `- ` bullets and table rows count, fenced lines are already blanked by `unfenced()`. Test: "excluded paths prose ignored".
3. Excluded file that another page links to → link still valid. Test: "link into excluded file".
4. Excluded path pointing at a `.private-terms` file → still never read (private check runs first). Covered by existing "private terms never read"; no new test.
5. Wiki with neither section (every 0.10.0 wiki) → identical output to 0.10.0, no info line. Test: existing "healthy default" plus assertion that stdout has no `excluded` text.

---

### Task 1: Validator honours `## Excluded paths`

**Files:**
- Modify: `canonical/codebase/scripts/validate-wiki.py` (`Validator.__init__`, new `excluded()`, `run()`, `main()`)
- Test: `scripts/test-wiki-validator.py` (new `schema_section_cases()` called from `run()` next to `adoption_cases()`)

**Interfaces:**
- Produces: `Validator.excluded(self, schema: Page, paths: dict[str, Path]) -> list[str]` returning the valid globs; `Validator.infos: list[str]`; `Validator.glob_ok(self, schema: Page, number: int, glob: str, what: str) -> bool` (reused by Task 2).

- [ ] **Step 1: Write the failing tests**

Add `schema_section_cases()` in the style of `adoption_cases()`: each case builds `fixture(repo)`, applies a setup, runs the validator with `-I`, and checks exit code plus a substring of stdout+stderr. `EXCL = "\n## Excluded paths\n\n- `results/*-data/**`\n"` appended to `SCHEMA.md`, and a file `results/run-data/report-1.md` containing `# no frontmatter\n`.

| Case | Setup | Exit | Output contains |
|---|---|---|---|
| excluded report skipped | EXCL + report | 0 | `1 paths excluded` |
| report without exclusion | report only | 1 | `missing or unterminated frontmatter` |
| link into excluded file | EXCL + report + index body `[r](results/run-data/report-1.md)` | 0 | `1 paths excluded` |
| exclusion cannot hide Core map | SCHEMA gets `\n## Excluded paths\n\n- `**`\n` | 1 | `Excluded paths must not match SCHEMA or Core map pages` |
| unsafe exclusion glob | bullet `- `../x/*`` | 1 | `unsafe Excluded paths glob` |
| malformed exclusion bullet | bullet `- results/*` (no backticks) | 1 | `Excluded paths entry` |
| excluded paths prose ignored | EXCL with a prose line `Generated data, not pages.` before the bullet + report | 0 | `1 paths excluded` |
| no section, no info | none | 0 | must NOT contain `excluded` |

- [ ] **Step 2: Run to verify they fail**

Run: `python3 scripts/test-wiki-validator.py`
Expected: the new cases print `FAIL`, all existing cases `PASS`.

- [ ] **Step 3: Implement**

- `__init__`: `self.infos: list[str] = []`, `self.exclusions: list[str] = []`.
- `glob_ok(schema, number, glob, what)`: false and error `f"unsafe {what} glob; use a wiki-relative pattern without .."` when the glob is empty, absolute, or has a `..` part.
- `excluded(schema, paths)`: `self.section(schema, "excluded-paths", "Excluded paths", required=False)`; for each line starting with `- `: must fullmatch ``- `([^`]+)` `` else error `"Excluded paths entry must be - `<glob>`"`; keep globs that pass `glob_ok(..., "Excluded paths")`. Then, for SCHEMA and every Core map path that `is_file()`, if any glob matches its wiki-relative POSIX path, error `"Excluded paths must not match SCHEMA or Core map pages"` once and drop that glob. Other lines are ignored.
- `run()`: call `excluded()` right after `core_map()`; in the `rglob` loop, after the private-terms check, skip paths whose relative POSIX path matches a kept glob, counting them; if the count > 0 append `f"info: {count} paths excluded by SCHEMA"` to `self.infos`.
- `main()`: print each info line to stdout before the findings/pass message.

- [ ] **Step 4: Run to verify they pass**

Run: `python3 scripts/test-wiki-validator.py`
Expected: every line `PASS`, exit 0.

- [ ] **Step 5: Commit**

```bash
git add canonical/codebase/scripts/validate-wiki.py scripts/test-wiki-validator.py
git commit -m "feat(validator): honour SCHEMA Excluded paths"
```

### Task 2: Validator checks the shape of `## Page types`

**Files:**
- Modify: `canonical/codebase/scripts/validate-wiki.py` (new `page_types()`, call in `run()`)
- Test: `scripts/test-wiki-validator.py` (`schema_section_cases()`)

**Interfaces:**
- Consumes: `Validator.glob_ok` from Task 1.
- Produces: `Validator.page_types(self, schema: Page) -> None`.

- [ ] **Step 1: Write the failing tests**

`TYPES = "\n## Page types\n\n| Path | type |\n| --- | --- |\n| `project/*` | `Project` |\n"` appended to `SCHEMA.md`.

| Case | Setup | Exit | Output contains |
|---|---|---|---|
| valid page types | TYPES | 0 | (pass message) |
| page types wrong header | header `| Glob | Kind |` | 1 | `Page types table` |
| page types one cell | extra row `| `adr/*` |` | 1 | `Page types row` |
| page types unsafe glob | row `| `../x/*` | `X` |` | 1 | `unsafe Page types glob` |
| page types empty type | row `| `adr/*` |  |` | 1 | `Page types row` |

- [ ] **Step 2: Run to verify they fail**

Run: `python3 scripts/test-wiki-validator.py`
Expected: new cases `FAIL`, others `PASS`.

- [ ] **Step 3: Implement `page_types(schema)`**

Section `("page-types", "Page types", required=False)`, rows via `self.table()`. Header must equal `["Path", "type"]` else error `"unsupported Page types table; expected Path and type columns"`. Each row: two cells, type (backticks stripped) not `unresolved()`, else `"Page types row needs a glob and a type"`; glob (backticks stripped) through `glob_ok(..., "Page types")`. Called in `run()` after `excluded()`. Page `type` values are not checked.

- [ ] **Step 4: Run to verify they pass**

Run: `python3 scripts/test-wiki-validator.py`
Expected: all `PASS`.

- [ ] **Step 5: Commit**

```bash
git add canonical/codebase/scripts/validate-wiki.py scripts/test-wiki-validator.py
git commit -m "feat(validator): check SCHEMA Page types shape"
```

### Task 3: Schema and workflows for exclusions and page types (A, C)

**Files:**
- Modify: `canonical/codebase/default-schema.md` (`## Page frontmatter`)
- Modify: `canonical/codebase/maintainer.md` (`## Page conventions`, type rule)
- Modify: `canonical/codebase/workflows/wiki-sync.md` (Step 2 exclusion line ~78; Step 4 `type` bullet)
- Modify: `canonical/codebase/workflows/wiki-lint.md` (Step 2 gather facts; `### Frontmatter hygiene`)
- Modify: `canonical/codebase/workflows/wiki-ingest.md` (Step 5), `wiki-init.md` (Step 4 adopt, Step 5 new)

- [ ] **Step 1: default-schema.md**

Under `## Page frontmatter`, after the default-type table, one paragraph each, as prose (no live sections in the default schema): optional `## Excluded paths` (bullets `` - `<glob>` ``, `fnmatch` on the wiki-relative path where `*` also crosses `/`, SCHEMA and Core map files cannot be excluded, OKF note that excluded `.md` files stay non-conformant unless they carry `type:`); optional `## Page types` (`Path | type` table, first match wins, falls back to the defaults above, put specific rows first). Each with a fenced example from the spec.

- [ ] **Step 2: maintainer.md**

`type:` rule: "Defaults by location, unless SCHEMA `## Page types` maps the path (first matching row wins)". New bullet: files matched by SCHEMA `## Excluded paths` are not wiki pages: never read, written, linted or synced as pages.

- [ ] **Step 3: Workflows**

- sync Step 2 (`Filter out paths excluded by ...`): name SCHEMA `## Excluded paths`.
- sync Step 4 and ingest Step 5: infer `type` from SCHEMA `## Page types`, then defaults.
- lint Step 2: skip excluded paths; `### Frontmatter hygiene`: `type` differing from the SCHEMA/default expectation is `info` (an explicit override is legal).
- init Step 4 (adopt): when the adopted folders do not match defaults, propose a `## Page types` table and an `## Excluded paths` list for generated reports in the Step 3 proposals message; write them only on confirmation. Step 5 new wiki: nothing.

- [ ] **Step 4: Verify**

Run: `python3 scripts/generate-codebase-packages.py && bash scripts/check-generated.sh`
Expected: no hardcoded-`wiki/` failure, "up to date" after the regeneration.

- [ ] **Step 5: Commit** (canonical files and regenerated packages)

```bash
git add canonical plugins skills .claude-plugin
git commit -m "feat: document Excluded paths and Page types in schema and workflows"
```

### Task 4: `verified` freshness, `generated` criterion, `unknown` migration (B, D, E)

**Files:**
- Modify: `canonical/codebase/maintainer.md` (`verified:` and `generated:` rules)
- Modify: `canonical/codebase/default-schema.md` (actor/trust paragraph)
- Modify: `canonical/codebase/workflows/wiki-lint.md` (`### Staleness`, trust summary in Step 4 report)
- Modify: `canonical/codebase/workflows/wiki-sync.md` (Step 4 frontmatter bullet, Step 6)

- [ ] **Step 1: maintainer.md and default-schema.md**

- `verified:` entries may carry an optional `commit: <sha>` (humans or the declared process write it; agents never).
- `generated:` changes only when the page's claims change (facts, commands, evidence paths, status); link, formatting, reordering and metadata-only edits leave it alone. A legacy page touched only in metadata keeps `updated` and gets no `generated`.

- [ ] **Step 2: wiki-lint.md `### Staleness`**

Add *Stale verified* (warning): per `verified` entry, with `commit` → stale if `git log <commit>..HEAD -- <sources>` is non-empty; without → stale if `git log --since=<at> -- <sources>` is non-empty; unresolvable commit or non-datetime `at` → info "freshness undetermined". A page counts as stale verified when every entry giving its tier is stale. Never change the tier. Summary line becomes `- Trust: unverified <n>, machine-confirmed <n>, human-reviewed <n> (stale verified <n>)`.

- [ ] **Step 3: wiki-sync.md**

- Step 4 frontmatter bullet: replace "set `generated`" with the claim-change criterion from Step 1.
- Step 6: when sync touches a tracker or baton row whose required cell reads `unknown`, replace it with the now-known value or `Not verified - <reason>`; no bulk migration.

- [ ] **Step 4: Verify**

Run: `python3 scripts/generate-codebase-packages.py && bash scripts/check-generated.sh`
Expected: "up to date".

- [ ] **Step 5: Commit**

```bash
git add canonical plugins skills .claude-plugin
git commit -m "feat: verified freshness, generated change criterion, unknown migration"
```

### Task 5: Release 0.11.0

**Files:**
- Modify: `canonical/codebase/VERSION`, `.claude-plugin/marketplace.json` → `0.11.0` (marketplace may be regenerated; check after generation)
- Modify: `docs/release-checklist.md` (new top section `## 0.11.0 field feedback`)

- [ ] **Step 1: Bump and regenerate**

Run: `python3 scripts/generate-codebase-packages.py && grep -rn '"version"' .claude-plugin plugins/*/plugin.json plugins/*/.codex-plugin/plugin.json`
Expected: every codebase plugin at `0.11.0`.

- [ ] **Step 2: Full suite**

Run: `bash scripts/run-tests.sh`
Expected: exit 0, including the four "standalone fixtures and byte equality passed" lines.

- [ ] **Step 3: Application scenario (not a real-host trial)**

In the scratchpad build a wiki with numbered folders (`00-project/`, `50-benchmark/results/run-data/report-1.md` without frontmatter, `adr/0001.md`), SCHEMA with both sections, and a git repo where one page's source is committed after its `verified.at`. Run the canonical validator (expect exit 0 and `1 paths excluded`), then walk the lint and sync instructions by hand and record: excluded file ignored, expected `type` from the table, stale verified counted, tier unchanged.

- [ ] **Step 4: Release checklist entry**

Record what was verified (suite result, fixture count, scenario outcome labelled as application scenario), commit SHA, and that real-host trials remain pending. Note feedback 4 as not reproduced.

- [ ] **Step 5: Commit**

```bash
git add canonical/codebase/VERSION .claude-plugin plugins skills docs/release-checklist.md
git commit -m "chore: release 0.11.0"
```

Main fast-forward, tag and push happen only on the user's explicit go-ahead.
