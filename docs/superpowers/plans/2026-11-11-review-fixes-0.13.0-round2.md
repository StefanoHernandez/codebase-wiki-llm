# 0.13.0 — round 2 fixes (after review)

> **For the implementer (Cursor):**
> - Branch `fix/review-0.13`. One commit for all items, or one per group; tests first where there is logic.
> - Same Global Constraints as `2026-11-11-review-fixes-0.13.0.md`: edit `canonical/` and `scripts/` only, regenerate packages, `git add` by path, never touch `SPEC.md`, never push `main` or tag.
> - Push the branch when done.

Review result: merge after fixes. The validator logic is sound, and the text output of every existing fixture is unchanged. On a copy of the Versal wiki, the only difference between 0.12.0 and 0.13.0 is the version in the suffix.

**Python for the tests on macOS:** `/usr/bin/python3` is 3.9. Run the suite with `PATH="$PWD/.venv/bin:$PATH" bash scripts/run-tests.sh` (the repo's `.venv` has 3.14).

## Important

1. **Committed bytecode.**
   - Problem: `scripts/__pycache__/test-wiki-validator.cpython-314.pyc` is committed.
   - Fix: run `git rm --cached` on it and add `__pycache__/` to `.gitignore`.
2. **CI fails on macOS** (runs 42929962160 and earlier).
   - Problem: `scripts/test-remind-wiki-sync.sh:30` uses `timeout`, which GitHub's macOS runners don't have (exit 127).
   - Fix: in `.github/workflows/test.yml`, before the test step, add a step with `if: runner.os == 'macOS'` that runs `brew install coreutils` and `echo "$(brew --prefix coreutils)/libexec/gnubin" >> "$GITHUB_PATH"`. Keep the test script unchanged.
3. **The templates test erases the markers** (`scripts/test-wiki-validator.py` ~789).
   - Problem: `re.sub(r"<[^>]+>", "text", body)` also replaces the `<!-- wiki:… -->` markers, so the "shipped templates form a valid current wiki" test never checks them.
   - Fix: use `r"<(?!!--)[^<>\n]+>"`, rerun the test, and fix any template the corrected test shows to be wrong.
4. **New contradiction: reserved rule vs adopt.**
   - Problem: `rules/wiki-context.md` "Reserved to people" forbids writing `accepted:` without a person. `workflows/wiki-init.md` (format upgrade) tells adopt to copy `accepted: <who>, <where>, <date>` when the existing record states it.
   - Fix (decision): copying an approval the record already states is recording, not deciding. That matches `maintainer.md` rule 14: "recording existing approval needs no repeat permission". Add to the reserved rule: "Copying an approval that an existing record already states (who, where, when), as adopt and sync do, is recording, not deciding."

## Minor

5. **⚫ closer names** (`validate-wiki.py` ~55, ~614).
   - Reject a closer that starts with `process:`, because ⚫ is reserved to people.
   - Reject a closer whose lowercase form matches `^(claude|gpt|gemini|codex|copilot|cursor|composer|antigravity)([-\s]?(code|opus|sonnet|haiku|fable|pro|flash|agent|\d[\w.]*))?$`, or that equals `ai agent` / `claude-code`.
   - Keep accepting `Claude Dupont`.
   - Add tests for `claude-code`, `GPT-5`, `Claude Opus`, `AI agent` and `process:ci` (all rejected), and for `Claude Dupont` (accepted).
6. **PLACEHOLDER HTML exemption** (`validate-wiki.py` ~42).
   - Exempt a tag name only when it is followed by `\s*/?>` or by an attribute (`\s+[\w-]+=`).
   - Tests: `<summary of the change>` and `<code path>` rejected; `<br>`, `<br/>` and `<span class="x">` accepted.
7. **`generated` shape.** A one-entry list `generated: [{ … }]` is rejected: require the bare `{}` shape. Test it.
8. **Typo in `default-schema.md` ~85.** The fixed token becomes `` `closed by <person> YYYY-MM-DD; not proven:` ``, without the space before `;`.
9. **Wording in `wiki-init.md` ~203.** Replace the sentence with "Keep the `format_version` the default schema carries."
10. **`docs/release-checklist.md`.**
    - 0.12.0: the Linux-tests item becomes "closed by 0.13.0 (CI matrix)" with the run link of the green run, after item 2.
    - 0.13.0: add the green CI run link, and add "macOS: run the suite with a Python ≥3.10 `python3` first on PATH".
11. **Weak JSON tests** (`test-wiki-validator.py` ~388+).
    - "json configuration error" asserts the full exit-2 document: exact key set, `wiki is None`, all three lists empty.
    - The upgrade-code check maps each message prefix to its expected code from the plan table, not just set membership.
12. **`Log order` row** (`validate-wiki.py` `profile`).
    - Match the setting name case-insensitively, after stripping `*` and backticks.
    - A row with more than two cells is read from the first two.
    - Test: `| **Log order** | newest first |` → valid.

## Done when

- `PATH="$PWD/.venv/bin:$PATH" bash scripts/run-tests.sh` exits 0.
- The GitHub `test` workflow is green on all four matrix jobs (link it in the final message).
- `git ls-files | grep __pycache__` prints nothing.
