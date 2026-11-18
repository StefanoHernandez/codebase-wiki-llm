# Legacy and v1 wikis

Read this file only when SCHEMA has no `## Core map` or no `format_version`,
when the validator prints `upgrade:` lines, or during `/wiki-init --adopt`.
A wiki already at the current format never needs it.

## v1 wiki (SCHEMA without `## Core map`)

Until `/wiki-init --adopt <root>` runs, use these paths under `<wiki-root>/`:

| Role | v1 path |
| --- | --- |
| index | `index.md` |
| log | `log.md` plus `agent/activity.md` |
| tracker | `project/work-tracker.md` |
| decisions | `project/decisions.md` |
| risks | `project/risks.md` |
| context | `agent/context.md` |
| handoff | `agent/handoff.md` |
| troubleshooting | `engineering/troubleshooting.md` |
| glossary | `glossary.md` |

- `/wiki-sync` and `/wiki-ingest`: locate core pages through these paths and
  suggest `/wiki-init --adopt <root>` in the report.
- `/wiki-lint`: a SCHEMA without `## Core map` is a v1 wiki (old
  `overview.md`, `agent/`, `project/` layout); check it against these paths
  and suggest `/wiki-init --adopt <root>`.
- After an adopt, a Core map row `activity (v1)` is part of the `log` (not an
  orphan) until it is merged; lint suggests merging it.

## Legacy page metadata

- Pages that have `updated` and none of the newer fields (`type`,
  `description`, `status`, `generated`) stay valid. Lint reports them as
  `info`; `/wiki-sync` upgrades them when it touches the page.
- A legacy page touched only in metadata keeps `updated` and gets no
  `generated`; `updated` is replaced by `generated` at the first change of
  the page's claims.
- Where a rule reads `generated.at`, a legacy page's `updated` is the fallback.

## Legacy tracker rows

Legacy Done rows without `Status` remain valid when their criteria are
proven. New Done rows always have `Status`.

## Gradual recovery after adoption

Rules added in 0.9.0 for code state on log entries and `## Approval` on
decisions apply to content written after the wiki adopted them. Lint
summarizes older omissions once as counts (for example `12 log entries
without code state`), respecting the Decisions exception and the local log
policy. Required metadata, readable tracker layouts and completion proof are
not exempted from validation. Missing legacy criteria remain recovery gaps;
normalizing columns or adding metadata does not make old outcomes newly
verified. Group gaps without duplicating deterministic findings.

Lint groups adopted pages without frontmatter by count and paths, one root
finding per page; it does not repeat missing-field/date/confidence checks for
absent metadata or count the deterministic finding twice. Report gradual
recovery as incomplete validation, including when structural adoption
succeeded.
