# Codebase Wiki LLM v2 — design

Date: 2026-09-30 · Status: draft, awaiting review · Target version: 0.9.0

## Purpose

Codebase Wiki LLM is a public plugin for software engineers (Claude Code,
Codex, Antigravity). The wiki exists for three things, in this order:

1. **shared context** between the people and the agents working on a repo;
2. **a log** of what was done, when, by whom, with what evidence;
3. **decisions** and why they were taken.

Everything else is optional and chosen per project.

v2 is modelled on a hand-built wiki that worked well in practice (an embedded
R&D project): evidence with command output and date, `⚠️ NOT VERIFIED`,
stable activity IDs with a single source of status, one results page per
session, a verified-facts table, and a confidentiality rule.

## Non-goals

- No JSON/YAML config file. Configuration is plain files (see *Configuration*).
- No automatic wiki writing from scripts. Hooks remind; the agent writes.
- No per-tool or per-file-save hooks.
- No multi-machine features.

## Configuration

Configuration lives in plain files, split by who reads them.

| Reader | What | Where | Format |
|---|---|---|---|
| scripts / hooks | wiki folder | `.wikidir` (repo root) | one line, unchanged from v1 |
| scripts / hooks | forbidden terms | `<wiki-root>/.private-terms`, git-ignored | one term per line, `#` comments |
| agent | project profile, core map, topics, conventions, budgets | `<wiki-root>/SCHEMA.md` | Markdown tables |

- `.wikidir` keeps its current rules and resolver; nothing breaks for v1 users.
- `.private-terms` must never be committed: the forbidden terms would leak
  through the file meant to protect them. `SCHEMA.md` records only that the
  rule is on and where the file is.
- `/wiki-init` writes these files. Afterwards the user edits them or asks the
  agent ("archive the log by release", "add a benchmark section"); both are
  equivalent. When the agent adds a topic or changes a convention it records
  it in `SCHEMA.md`, so sync and lint pick it up.

### `SCHEMA.md` sections

1. **Project profile** — language, project division (phases/WP, releases,
   sprints/milestones, none), sensitive data on/off, active topics.
2. **Core map** — role → path table. Every command locates core pages through
   this table, never through hard-coded paths.
3. **Conventions** — ID prefix (default `T`), status icons (default
   🟢 done and verified · 🟡 in progress · ⚪ to do · 🔴 blocked, where 🔴 means
   "work stopped", not "serious"), evidence format.
4. **Budgets** — size thresholds (defaults below).
5. **Topics** — one row per topic folder/page and what belongs there.

## Core

Default layout for a new wiki (paths are the Core map defaults):

```text
<wiki-root>/
├── index.md             map + status table (cites IDs, never repeats status)
├── SCHEMA.md            configuration for the agent
├── log.md               recent log
├── log/                 log archives, one per closed phase/release/sprint/quarter
├── project/
│   ├── work-tracker.md  only source of status; stable IDs, never reused
│   ├── decisions/       one decision per file: 0001-<slug>.md
│   └── risks.md
├── agent/
│   ├── context.md       fast onboarding for a new agent or person
│   └── handoff.md       baton: state, next steps, what not to redo
├── troubleshooting.md   symptom · cause · fix · evidence
├── glossary.md          terms, acronyms, internal names
└── <topics>/            chosen at init, e.g. architecture/, environment/, operations/
```

Changes from v1:

- **One log.** `log.md` and `agent/activity.md` merge; each entry names its
  author (`human` or `agent`).
- **Decisions as files** instead of a single `decisions.md`.
- **`engineering/`, `modules/`, `project/status|roadmap|milestones|requirements`,
  `project-docs/` leave the core** and become optional topics.
- **`troubleshooting.md` and `glossary.md` join the core.**

### Mandatory sections of `agent/context.md`

- Goals and **non-goals**
- Non-negotiable rules / invariants
- Frequent commands (setup, build, test, lint), verified ones marked
- **Verified facts**: fact · value · evidence · date; plus "errors already
  corrected, do not reintroduce"
- Read first: at most 5 links

### Log entry format

```markdown
## 2026-09-29 · <title> · agent
- What: …
- Evidence: `<command>` → <essential output> (or `> ⚠️ NOT VERIFIED`)
- IDs: T27
```

Never write invented output "by way of example" next to real output.

## `/wiki-init`

1. **Read-only survey**: existing docs (`docs/`, `wiki/`, count of `.md`),
   `CLAUDE.md`/`AGENTS.md`, README language, project-type signals, `.gitignore`.
2. **One message with pre-filled, numbered proposals.** The user replies `ok`
   or overrides by number (`3: releases, 5: yes`). No one-question-at-a-time:
   it is slow and Codex/Antigravity have no question UI.
   1. Folder: adopt existing docs, or new `wiki` / `.wiki`.
   2. Wiki language.
   3. Project division: phases/WP · releases · sprints/milestones · none.
   4. Topics: pre-checked from the survey (architecture pre-checked for most
      software repos).
   5. Sensitive data: no / yes → forbidden terms, local-only paths (verified
      with `git check-ignore -v`), git pre-commit check.
   6. Agent entry file: thin `CLAUDE.md`/`AGENTS.md` pointing to
      `agent/context.md`. Existing file: never overwritten; propose trimming
      duplicated status only.

   Conventions and budgets are shown as defaults, not asked.
3. Write only after confirmation.

### Adopt mode

Triggered when the survey finds an existing docs folder, or by
`/wiki-init --adopt <folder>`.

- Writes `.wikidir` and `SCHEMA.md`; the Core map points to existing files
  (e.g. log → `00-project/project-log.md`, decisions → `adr/`).
- Proposes creating only the missing core roles.
- Never moves or renames files without confirmation.
- Replaces the v1 rule "the folder must not already contain files".

### v1 wikis

A v1 wiki (has `SCHEMA.md` but no Core map) is handled by adopt mode on the
same folder: the Core map maps v1 paths (`project/decisions.md`,
`agent/activity.md`, …). Merging `agent/activity.md` into the log is proposed,
not done silently. Sync and lint on a v1 wiki without a Core map keep working
with v1 default paths and suggest running adopt.

## `/wiki-sync`

Keeps the v1 mechanism (`git diff`, `source_commit` per page). Adds:

- **Log**: append one entry (format above).
- **Tracker and handoff**: update touched IDs; rewrite `handoff.md`.
- **Decisions**: if the change embodies a choice (new dependency, architecture
  change, rejected alternative), *propose* `decisions/NNNN-<slug>.md`.
- **Troubleshooting**: if the session solved a problem, *propose* an entry.
- **Log archive**: when a phase closes (per the project division) or `log.md`
  exceeds its budget, *propose* the cut: entries up to that date move to
  `log/<phase>.md`, `log.md` keeps a link. Cut by date, not by topic, because
  phases overlap in time and one entry can touch two phases.

## `/wiki-lint` (read-only)

| Check | Flags |
|---|---|
| Evidence | technical claims or verified facts without date or command; output without the command that produced it |
| Verified facts | facts whose sources changed after their verification date |
| Single status | status icons outside the tracker (except pages that declare otherwise, e.g. risk severity); IDs cited but missing; duplicated or reused IDs |
| Core map | roles pointing to missing files; broken links |
| Handoff | handoff older than the recent commits |
| Budget | page > 20 KB; per-session read set > 40 KB; `log.md` > 30 KB or holding entries of a closed phase |
| Confidentiality | `.private-terms` hits in tracked files; local-only paths not ignored; sensitive profile without `.private-terms`; missing git pre-commit check (offer to install) |

Per-session read set: `CLAUDE.md`/`AGENTS.md`, `index`, `agent/context`,
`agent/handoff`, tracker, `log.md`. Thresholds are defaults in `SCHEMA.md`.

The agent runs these checks with `wc -c`, `grep`, `git`. Only the forbidden
terms check is a script, because the git hook needs it deterministic.

## Hooks

One POSIX `sh` script per hook, in `canonical/codebase/scripts/`, copied into
each host package by the generator (as the resolver is today).

| Hook | Event | Behaviour | Claude | Codex | Antigravity |
|---|---|---|---|---|---|
| Resolver (exists) | session start | prints `wiki_root: <value>`; adds "handoff is N commits old" when stale | SessionStart | **new**: `.codex-plugin/plugin.json` `"hooks"` → same hooks file | none (no SessionStart); the always-on rule resolves the root |
| Sync reminder (new) | agent about to stop | if files outside the wiki changed and the wiki did not, ask the agent to run `/wiki-sync` or say why not | Stop | Stop | Stop, `decision: "continue"` |
| Forbidden terms (new, opt-in) | `git commit` | block the commit when staged content matches `.private-terms` | git `pre-commit` | same | same |

- The sync reminder fires once: on Claude it exits quietly when
  `stop_hook_active` is true, so an answer like "only a test refactor" ends
  the turn. It is silent when there are no changes outside the wiki.
- Antigravity runs hooks with cwd = plugin directory; the script takes the
  repo path from `workspacePaths` in the stdin JSON.
- The forbidden-terms check is a git hook, not an agent hook, because people
  commit too. `/wiki-init` installs it only with sensitive data on; since
  `.git/hooks` is not versioned, `/wiki-lint` offers to install it in a new
  clone.

## Cross-host maintenance

Primary constraint: one change must reach Claude Code, Codex and Antigravity
without editing three places.

- **One source.** All prompt content lives in `canonical/`; all scripts in
  `canonical/codebase/scripts/`. Host packages under `plugins/` and `skills/`
  are generated, committed, and never edited by hand.
- **Host differences only in the generators**: file layout (commands vs
  skills vs rules), manifest shape, hook wiring. No host-specific wording in
  `canonical/`.
- **One version per plugin.** A one-line file per plugin,
  `canonical/codebase/VERSION` and `canonical/secondbrain/VERSION`, feeds
  every manifest, including `.claude-plugin/marketplace.json`, which becomes
  generated (today it is edited by hand and the version is written four times).
  Release = edit `VERSION`, run `python3 scripts/generate-host-packages.py`,
  commit.
- **One hooks file for Claude and Codex** (same format), wired from both
  manifests; Antigravity gets its own generated `hooks.json` calling the same
  scripts.
- **Drift guard.** `scripts/check-generated.sh` also covers the marketplace
  file and the hook files, and runs as a git `pre-commit` hook in this repo
  (installed by a one-line `scripts/install-dev-hooks.sh`), so stale generated
  files cannot be committed.
- **Adding a host later** = one new `generate_<host>()` function; canonical
  content is untouched.

## Testing

- Extend `scripts/test-resolve-wiki-root.sh` for the stale-handoff line.
- New `sh` tests for the sync reminder (changes outside wiki / only wiki /
  none / `stop_hook_active`) and the forbidden-terms check (hit, no hit,
  missing file, comments, case-insensitive).
- `scripts/check-generated.sh` covers the new generated files.
- `scripts/validate-agent-handoff.py` reads the Core map when present,
  falling back to v1 paths.
- Manual run on a scratch repo per host: init (new), init (adopt), sync, lint.

## Open points to verify during implementation

- Codex `Stop` hook support and payload fields.
- Antigravity `Stop` payload: exact shape of `workspacePaths`.
- Whether Codex expands `${CLAUDE_PLUGIN_ROOT}` (ponytail's shared hooks file
  suggests it does).
