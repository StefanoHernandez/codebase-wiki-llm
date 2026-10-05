# Release checklist

## 0.9.2 adoption compatibility patch

This patch addresses the adoption feedback forwarded by Stefano on 2026-10-01.
The reported shape (47 pages without metadata, older tracker columns, absent
archive) was reproduced in a synthetic fixture, not by inspecting the target
project. The 0.9.1 validator produced 431 findings; the corrected fixture
expects 50 root/gap findings and exit 1, retaining incomplete validation.

- [x] Full automated suite passes on the patch commit.
- [x] Independent code review and workflow application scenarios complete;
  material findings resolved.
- [x] Main and `v0.9.2` pushed; remote SHAs verified.

Verified on 2026-10-02 at release commit
`e4bf94ffa936edc9adca3e0fb03edbe15d6a51db`:
`bash scripts/run-tests.sh` exited 0, including 102 validator fixtures on the
canonical script and all four byte-identical standalone distributions, plus
the existing generator, continuity, reminder, privacy and hook checks.
Independent read-only code review found no unresolved material issues.
Five workflow application scenarios covered gradual adoption, explicit
re-adoption, a hash-free log, rewritten history and incomplete full recovery;
the historical-closure ambiguities they found were corrected and rechecked.
These application exercises are not real-host trials.

Remote verification confirmed main and peeled `v0.9.2` at the release commit
above; the annotated tag object is
`ce3d24fb4eac96b5d0b91edb3ef2afe4a33f6a78`. Later documentation-only commits
may advance main without changing the tagged plugin files.

Following Stefano's requested ordering, automated checks and publication
precede further real-project trials. The forwarded adoption attempt is
evidence of defects in 0.9.1, not proof that the corrected workflows work on
all hosts. Real-host compatibility rows below remain pending.

Next field trial: rerun `--adopt` on the existing numbered wiki without
rebuilding it, preserve the log's hash policy, confirm only the desired
tracker/metadata recovery, then record actual lint results and sync coverage.

## 0.9.1 release record

For Codebase Wiki LLM **0.9.1**, Stefano requested the following order:
automated checks and whole-branch review, integration and main/tag push,
then real-host field trials. All real-host rows below are explicitly
**pending** until those user trials; they are not prerequisites for this
patch's main push and are not reported as passed.

Record each trial on **Codex, Claude Code and Antigravity** in a real session
on a real project. Other harnesses (generic Agent Skills) come later.
Scripted tests and subagent runs do not replace these rows; record them
separately. This exception documents the requested 0.9.1 sequence rather
than changing the evidence needed for real-host compatibility claims.

## Automatic

- [x] `bash scripts/run-tests.sh` passes on the release commit.
- [x] Whole-branch review passes; material findings are resolved.
- [x] Main and `v0.9.1` pushed; remote SHAs verified before user field trials.

## Per host (real session)

Record host, host version, OS, date and commit for each run.
Current state: **pending on all three hosts; trials follow the main push**.

| Step | Codex | Claude Code | Antigravity |
| --- | --- | --- | --- |
| Install from the branch; the four commands or skills appear | | | |
| `/wiki-init` on a repo without docs: one-message survey (7 items, language asked), wiki written | | | |
| `/wiki-init --adopt <folder>` on a repo with docs: compatibility scope proposed, pages mapped in place, markers added, gaps explicit; optional moves accepted or skipped, respecting an earlier no | | | |
| Explicit `--adopt` on an already mapped wiki: recover approved gaps in place without rebuilding the scaffold | | | |
| Adopt older pages without frontmatter and a custom tracker: gradual recovery preserves evidence and IDs, reports incomplete validation, and does not fabricate historical closure | | | |
| New session: `wiki_root` and `new context` lines (Codex, Claude Code) or the rule (Antigravity); the agent reads the core once | | | |
| Change code, send another message: the note appears once and does not block | | | |
| Antigravity: the note appears once per turn (initialNumSteps stays constant within a turn) and a quiet hook's {} output is accepted | n/a | n/a | |
| Codex: SessionStart and UserPromptSubmit plugin hooks run (${CLAUDE_PLUGIN_ROOT} resolves) | | n/a | n/a |
| `/wiki-sync`: log entry in project format, tracker row, handoff; first actual archive creates its directory and archiving follows budget | | | |
| Hash-free log policy or rewritten Git history: sync preserves conventions, validates anchors and reports incomplete coverage without a false nothing-to-do | | | |
| Switch participant or host mid-task: the next agent continues from the handoff without redoing work | | | |
| `/wiki-lint`: report with no false alarms on a healthy wiki | | | |
| `/wiki-lint`: installed deterministic validator runs; missing or older Python explicitly skips it while read-only review continues | | | |
| Edit a source twice with wiki coverage between edits: second edit prompts a new note | | | |
| Human unproven closure stays ⚫ with authority and evidence; verified completion stays 🟢 | | | |

## Field measures (compare with the situation before the plugin)

- Time to orient and reach the first verified change.
- Stale or contradicted claims found by `/wiki-lint`.
- Analyses or attempts repeated after a handoff.
