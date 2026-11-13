# Changelog

Changes to **Codebase Wiki LLM**. The wiki format has its own number (`format_version` in
`SCHEMA.md`); `validate-wiki.py --version` prints both.

## 0.15.0

- SecondBrain Wiki LLM is no longer part of this repository: its packages, skills and
  marketplace entries are removed. The last version is in tag `v0.14.1` (SecondBrain 0.2.1). If
  you installed it, uninstall it (`/plugin uninstall secondbrain-wiki-llm@stefano-wiki` in Claude
  Code). Codebase Wiki LLM is unchanged; format stays `0.12.0`.

## 0.14.1

- The context rule no longer mentions `search_wiki`, which the Codebase Wiki
  app's MCP server stopped offering: `search_code` is for where/how questions
  in source code; status, decisions, risks and why still come from the wiki.
  Format stays `0.12.0`.

## 0.14.0

- The tracker's optional `Depends on` column has a defined meaning: tracker
  IDs a task waits for and external conditions in free text. The validator
  reports a dependency on an ID that does not exist, a task that depends on
  itself and a cycle among open tasks. `/wiki-sync` puts ready tasks first in
  `## Next steps` and the baton. Format stays `0.12.0`.

## 0.13.1

- Optional local search: when the Codebase Wiki desktop app's `codebase-wiki`
  MCP server is connected, agents use `search_wiki` and `search_code` to find
  pages and code before grepping. Without it nothing changes. Format stays
  `0.12.0`.

## 0.13.0

- The wiki format has its own number. This release keeps format `0.12.0`: a
  wiki already at `format_version: 0.12.0` has nothing to upgrade.
  `validate-wiki.py --version` prints the release and the format.
- `validate-wiki.py --json <wiki-root>` prints one JSON document for tools.
- A handoff that lags behind a tracker change made by a person is reported as
  `info:`, not as a finding.
- Fewer false positives (autolinks, generics, footnotes, proposals that
  mention an ID, translated tables with extra columns); a page that cannot be
  read is one finding with its path.
- New checks: shape of `generated` and `verified`, agent names in a ⚫
  closure, duplicate decision numbers, the optional `Log order` setting.
- The rules reserved to people are in the always-loaded rule.

## 0.12.0

- SCHEMA declares `format_version`. The validator prints `upgrade:` lines
  when a wiki is older than the plugin (missing version, legacy Done table,
  decision status in the body, no `## Approval`, missing SCHEMA sections);
  they never change the exit code. `/wiki-init --adopt <wiki-root>` applies
  the upgrade and raises `format_version` only when no line remains.
- New default structures, each behind a marker that tools can read: the index
  `wiki:owners` table (one topic, one page), tracker `## Next steps`
  (`wiki:next`), the risks register (`wiki:risk-register`, IDs `R<n>`, fixed
  severities) and decision `## Approval` (`wiki:approval`).
- `verified` is written on one line.

## 0.9.2

- Adoption inventories missing metadata, incompatible tracker tables and
  local conventions before proposing edits. Gradual recovery keeps gaps
  explicit; adopting the structure does not certify old content.
- Missing frontmatter produces one finding per page. An unreadable Open
  tracker reports unavailable handoff reference checks without cascading
  missing-ID errors; baton fields and links are still checked.
- The log archive directory is created at the first archive write; its
  reserved path must remain safe and creatable.
- Existing project log rules take precedence, including bans on commit
  hashes. Sync validates Git anchors and reports incomplete committed-change
  coverage when a usable baseline is absent or history has been rewritten.
- Regression fixtures include 47 pages without metadata and legacy tracker
  columns, in addition to current templates at adopted paths.

## 0.9.1

- Reminder coverage tracks source content: another edit at a covered path or
  a path already dirty at session start prompts another next-turn note.
- Every maintainer distribution ships a standalone deterministic wiki
  validator. `/wiki-lint` runs it before the agent's semantic review.
- Tracker terminal rows distinguish 🟢 verified completion from ⚫ work a
  person explicitly closed without proven criteria. Handoff cites tracker IDs.
- Already approved decisions can be recorded as `accepted` with who, where
  and when; new unresolved ideas remain `proposed`.
- Automated checks precede the main/tag push. Real-host Codex, Claude Code
  and Antigravity trials remain pending until Stefano's trials after the push:
  [release checklist](docs/release-checklist.md).

## 0.9.0

- v2 core: a small fixed core (index, log, tracker, decisions, risks, context,
  handoff, troubleshooting, glossary) located through the `SCHEMA.md` Core map.
- One log: `agent/activity.md` is merged into `log.md`.
- The project-docs, engineering and overview pages and the export are no longer
  built in; add them as topics when you need them.
- Hooks: SessionStart resolves the wiki root, asks for one full core read at a
  new context and flags a stale handoff; a note at your next message (never a
  block) says when changed code is not covered by the wiki.
- Evidence proportional to the claim, with the code state (`@<sha>`,
  `+local`); a fact that can no longer be proven is marked `⚠️ TO RE-VERIFY`.
- Tracker with goal, done criteria and a separate Proposals list; 🟢 only with
  proven criteria. Decisions stay `proposed` until a person approves them.
- Pages in the language you choose; stable `<!-- wiki:… -->` markers keep the
  checks working.
- Adopt maps existing docs in place, then proposes a migration plan as one
  numbered list, each move accepted or skipped; `/wiki-sync` archives the log
  by rule.
- Release gate: [docs/release-checklist.md](docs/release-checklist.md).
- v1 wikis keep working; run `/wiki-init --adopt <folder>` to move to v2.
