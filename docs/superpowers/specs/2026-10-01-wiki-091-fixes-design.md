# Codebase Wiki LLM 0.9.1 — reliability fixes

Date: 2026-10-01. Scope approved by Stefano in the chat: apply the four
reviewed corrections, run automated checks and review, merge and push to
`main`, and publish tag `v0.9.1`. Real-host field checks follow that push;
they must remain explicitly pending rather than being reported as passed.

## Goal

Keep the wiki useful to existing engineers, newcomers, coding agents and
work-management agents by making change coverage repeatable, structural
validation available to installed users, and status and authority unambiguous.

## 1. Reminder coverage identifies a file state

The next-turn note stays non-blocking. Store a content fingerprint alongside
every baseline or covered source path. Exclude a path only while its current
fingerprint matches the stored one. A second edit after wiki coverage, or an
edit to a source already dirty at session start, must become eligible again.
Include current source fingerprints in notification deduplication so new
content at the same path is not mistaken for an unchanged state. Deleted
files must have a stable distinguishable state. Keep POSIX shell and Git
runtime requirements for hooks; no new dependency for hooks.

## 2. Installed structural validator

Add `canonical/codebase/scripts/validate-wiki.py`, distributed in each
maintainer skill's `scripts/` folder, including generic Agent Skills.
`/wiki-lint` runs it before its semantic analysis. Use Python 3.10+ and the
standard library only; document this optional lint dependency. If Python is
unavailable, report that the deterministic check was not run and continue
the agent's read-only review. Never install a runtime implicitly or claim
validation passed when unavailable.

The command accepts a wiki directory and is read-only. Return 0 for valid
structure, 1 for findings and 2 for invocation/configuration failures. Print
actionable file/line diagnostics without reading or printing private terms.

Check the documented frontmatter format, required fields, non-empty titles,
real ISO dates, confidence values, source paths, relative Markdown file
links, Core map roles and paths, tracker ID uniqueness, continuity markers
and baton structure. Recognize stable markers with legacy English heading
fallback for existing wikis. Respect adopted paths through the Core map and
v1 defaults when the map is absent. Ignore fenced code examples and remote
links; do not claim to validate arbitrary YAML or every Markdown extension.
Sources are repository-relative and may name directories, use `./`, or carry
`:line` / `#symbol` suffixes. Resolve link paths relative to the containing
page, with URL decoding and fragments separated from file existence.

The schema is configuration: unlike content pages, it need not list sources.
Tracker proposals have no activity IDs; IDs may be referenced elsewhere but
must not be defined twice across Open and terminal rows. A no-work baton is
valid only if the mapped tracker has no open rows. The legacy continuity CLI
keeps its compatibility contract, and both entry points are tested.

Use actual path placeholders in templates, including handoff log/tracker
sources and decision frontmatter. Init must substitute the resolved Core map
paths before writing pages. Verify the packaged copy runs without this
repository's development scripts.

## 3. Closed without proof is distinct from verified completion

Add `⚫` for work explicitly closed by a person without proven criteria
(cancelled, unnecessary or accepted without verification). Reserve `🟢` for
completed and verified work. Terminal tracker rows explicitly carry a Status
column so they distinguish these outcomes. An unproven closure records
`closed by <person> YYYY-MM-DD; not proven: <what>`; an agent cannot invent
that authority. Preserve legacy proven Done rows without a Status column.
Lint flags a green row containing an explicit unproven closure, and a black
row missing its human closure evidence. Scripts check explicit structural
claims; semantic proof remains the agent/reviewer's responsibility.

## 4. Handoff and decision authority

Replace the handoff's generic `Status` field with `Tracker IDs`, pointing to
the tracker for activity status. Keep Git state and verified next steps.
An already approved decision is recorded directly as `accepted`, with who,
where and when. A new idea is `proposed`; only unresolved choices need user
input. Sync may create an accepted decision record without another approval
to document it. Do not invent approval, reasons or rejected alternatives.
Align maintainer, schema, sync, ingest, lint and templates with these rules.

## Release and limits

- Edit canonical sources; generate host packages and commit their output.
- Bump Codebase to `0.9.1`; leave SecondBrain unchanged.
- Add targeted regression fixtures before runtime implementation.
- Run the complete suite and a whole-branch review before integration.
- Do not mark live Codex/Claude/Antigravity checks complete without a run.
- Record Stefano's requested sequence in the release checklist: this patch
  goes to `main` for field trials; broad real-host validation follows.

## Acceptance

1. Repeated edits at one path and initially dirty paths produce the correct
   next-turn note; unchanged covered content remains quiet.
2. Installed validator accepts healthy default/adopted/localized wikis and
   rejects invalid dates, missing sources, broken links, unsafe Core paths,
   duplicate IDs, malformed baton sections and contradictory no-work state.
3. Green verified and black human-unproven closure fixtures remain distinct.
4. Handoff points to tracker IDs; accepted decisions require recorded human
   authority and can be documented without a repeated approval request.
5. All generated packages ship identical canonical validator content and
   version `0.9.1`; existing tests pass; real-host checks remain pending.
