# Release checklist

A release reaches `main` only when every row below passes on **Codex, Claude
Code and Antigravity**, each in a real session on a real project. Other
harnesses (generic Agent Skills) come later. Scripted tests and subagent runs
do not replace these rows; record them separately.

## Automatic

- [ ] `bash scripts/run-tests.sh` passes on the release commit.

## Per host (real session)

Record host, host version, OS, date and commit for each run.

| Step | Codex | Claude Code | Antigravity |
| --- | --- | --- | --- |
| Install from the branch; the four commands or skills appear | | | |
| `/wiki-init` on a repo without docs: one-message survey (7 items, language asked), wiki written | | | |
| `/wiki-init --adopt <folder>` on a repo with docs: pages mapped in place, markers added, migration plan proposed as one numbered list, each move accepted or skipped | | | |
| New session: `wiki_root` and `new context` lines (Codex, Claude Code) or the rule (Antigravity); the agent reads the core once | | | |
| Change code, send another message: the note appears once and does not block | | | |
| Antigravity: the note appears once per turn (initialNumSteps stays constant within a turn) and a quiet hook's {} output is accepted | n/a | n/a | |
| Codex: SessionStart and UserPromptSubmit plugin hooks run (${CLAUDE_PLUGIN_ROOT} resolves) | | n/a | n/a |
| `/wiki-sync`: log entry with `@<sha>`, tracker row, handoff; log archived when over budget | | | |
| Switch participant or host mid-task: the next agent continues from the handoff without redoing work | | | |
| `/wiki-lint`: report with no false alarms on a healthy wiki | | | |

## Field measures (compare with the situation before the plugin)

- Time to orient and reach the first verified change.
- Stale or contradicted claims found by `/wiki-lint`.
- Analyses or attempts repeated after a handoff.
