<!-- Generated from codebase/references/work-tracker-template.md. Do not edit directly. -->

# Work Tracker Template

Use this template for the `tracker` page (Core map). It is the only source of
status and connects project state to agent handoff tasks.

```markdown
---
title: Work Tracker
updated: YYYY-MM-DD
sources:
  - <wiki-root>/<Core map log path>
  - <wiki-root>/<Core map handoff path>
  - <source-files-or-plans>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Work Tracker

Only source of status. IDs (`T1`, `T2`, …) are stable and never reused. Other
pages cite IDs without repeating their status. Status icons: see SCHEMA.md
`## Conventions`. External issues and PRs are linked, never copied as status.

## Open
<!-- wiki:open -->

| ID | Status | Goal | Done when | Owner | Next verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | 🟡 | <outcome> | <observable criteria> | <person, agent or `unknown`> | `<command>` or <check> | <link or `⚠️ NOT VERIFIED - <reason>`> |

## Proposals
<!-- wiki:proposals -->

Ideas and suggested work nobody approved yet: no ID, no status icon.

| Proposal | By | Date | Why |
| --- | --- | --- | --- |

## Done
<!-- wiki:done -->

| ID | Goal | Closed | Criteria met | Evidence |
| --- | --- | --- | --- | --- |
```

Rules:

- Add `Phase` (when the SCHEMA project division is not `none`), `Priority` or
  `Depends on` columns only when they help.
- A person approves a proposal by moving it to Open with the next free ID.
  Agents add proposals; they never move one to Open themselves.
- A row moves to Done (🟢) only when every `Done when` criterion is met and
  proven with a check that fits the work: a test or command for code, a link
  or review for documents, a recorded outcome for management work. Limits stay
  explicit in `Criteria met`. A test that could not run is not a passed test.
- Agents update status and evidence of the rows they work on and mark a row 🔴
  with the reason when work stopped. Owners, deadlines, priorities and scope
  are human decisions.
- Keep this page compact; detail belongs in topic pages and the log.
- Link open work to the `handoff` page when another coding agent needs to
  continue it.
