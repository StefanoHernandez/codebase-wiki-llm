---
description: Deep-dive into a file, directory, feature, or topic and update the wiki.
---

<!-- Generated from codebase/workflows/wiki-ingest.md. Do not edit directly. -->

# /wiki-ingest [path]

Deliberate, focused update of the wiki based on a specific file, directory,
feature, or topic.

Argument:

- `[path]` can be a file path, directory, or topic.
- If omitted, ask what to ingest.

Requires the wiki maintainer skill. Respect `wiki/SCHEMA.md`.

## Step 1 - Preconditions

- If `wiki/` does not exist, tell the user to run `/wiki-init` first.
- If `wiki/SCHEMA.md` is missing, use defaults and warn the user.

## Step 2 - Resolve the target

- If the argument is an existing file or directory, use it.
- If it is a topic, search for relevant files, recent commits, tests, docs, and
  config. Ask only if ambiguous.
- Announce the resolved target before editing.

## Step 3 - Read evidence

Read the target and enough related files to understand it:

- directly relevant source files;
- imported/required files one level deep when needed;
- related tests;
- relevant config, migrations, CI, README, or project docs;
- existing wiki pages that mention the target.

Record key functions, types, flows, invariants, decisions, dependencies,
verification commands, and failure modes.

## Step 4 - Determine affected pages

Consider:

- `overview.md`;
- `engineering/architecture.md`;
- `engineering/data-model.md`;
- `engineering/development.md`;
- `engineering/testing.md`;
- `engineering/operations.md`;
- `engineering/troubleshooting.md`;
- `engineering/change-map.md`;
- `modules/<area>.md`;
- `project/status.md`, `project/roadmap.md`, `project/risks.md`,
  `project/requirements.md`, `project/decisions.md`;
- `project-docs/evidence.md` and other project-docs pages when reusable claims
  or proof points emerge;
- `agent/context.md`, `agent/activity.md`, `agent/handoff.md`;
- `glossary.md`;
- `index.md`;
- `log.md`.

List affected pages to yourself before editing.

## Step 5 - Update pages

For each affected page:

1. Read the current page.
2. Make the minimum accurate edit.
3. Update frontmatter: `updated`, `sources`, `source_commit`, `confidence`.
4. Add supersession notes when correcting old claims.
5. Preserve and add relative links where useful.

If creating a module page, use the module quality bar from the maintainer skill.

If creating or updating project-docs claims, link each claim to engineering,
project, or source evidence. Mark unsupported claims as gaps/hypotheses.

## Step 6 - Update index and log

Update `index.md` for any page added, removed, renamed, or materially retitled.

Append to `log.md`:

```markdown
## [YYYY-MM-DD] ingest | <short description>
- Target: <path or topic>
- Pages touched: <count>
- Pages created: <list>
- Pages updated: <list>
- Notable changes: <one or two bullets>
- Follow-up: <anything needing attention or none>
```

Append to `agent/activity.md` for non-trivial ingests.

## Step 7 - Report

Tell the user:

- what was ingested;
- pages created and updated;
- important engineering/project/project-docs findings;
- follow-up recommendations.

## Guardrails

- Never modify source code.
- Never delete pages during ingest; flag redundancy for lint.
- If more than half the wiki needs rewriting, stop and recommend a deliberate
  reorganization.
- Keep confidence honest.
