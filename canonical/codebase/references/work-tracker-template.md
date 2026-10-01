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
  - <source-path>
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

| ID | Status | Goal | Closed | Criteria met | Evidence |
| --- | --- | --- | --- | --- | --- |
```

Rules:

- Add `Phase` (when the SCHEMA project division is not `none`), `Priority` or
  `Depends on` columns only when they help.
- A person opens a task by moving a proposal to Open or by asking for the
  work in the conversation; the agent then writes the Open row with the next
  free ID and who asked. Agents never open a task on their own.
- A row moves to Done with Status 🟢 only when every `Done when` criterion
  is met and proven with a check that fits the work: a test or command for
  code, a link or review for documents, a recorded outcome for management
  work. `Criteria met` records the proof and `Evidence` cites it. A test that
  could not run is not a passed test.
- A person may explicitly close unproven work (cancelled, unnecessary or
  accepted without verification): move it to Done with Status ⚫.
  `Criteria met` reads `closed by <person> YYYY-MM-DD; not proven: <what>`;
  `Evidence` cites the human closure source. Agents cannot invent this
  authority or use 🟢 for an unproven closure. Without that closure, keep the
  row Open and name the missing proof.
- Legacy Done rows without a Status column remain valid for proven completion;
  write new terminal rows with Status to distinguish 🟢 and ⚫.
- IDs are unique across Open and Done; move a row rather than defining it twice.
- Resolve source placeholders to concrete repository-relative paths before
  writing; use the confirmed wiki root and Core map paths.
- Agents update status and evidence of the rows they work on and mark a row 🔴
  with the reason when work stopped. Owners, deadlines, priorities and scope
  are human decisions.
- Keep this page compact; detail belongs in topic pages and the log.
- Link open work to the `handoff` page when another coding agent needs to
  continue it.
