# /wiki-ingest [path]

Deliberate, focused update of the wiki based on a specific file, directory,
feature, or topic.

Argument:

- `[path]` can be a file path, directory, or topic.
- If omitted, ask what to ingest.

Requires the wiki maintainer skill. Respect `<wiki-root>/SCHEMA.md`.

## Step 0 - Resolve the wiki root

{{include:partials/resolve-wiki-root.md}}

## Step 1 - Preconditions

- If Step 0 found no wiki, tell the user to run `/wiki-init` first.
- If `<wiki-root>/SCHEMA.md` is missing, use defaults and warn the user.

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

Locate core pages through SCHEMA `## Core map`; fall back to v1 paths
(`engineering/`, `project/`, `agent/`) only when it is missing.

Consider:

- the `index`, `context`, `handoff`, `tracker`, `decisions`, `risks`,
  `troubleshooting` and `glossary` pages, and the `log`;
- the topic pages listed in SCHEMA `## Topics`;
- `modules/<area>.md`.

A new topic page must be listed in SCHEMA `## Topics`: add the row.

List affected pages to yourself before editing.

## Step 5 - Update pages

For each affected page:

1. Read the current page.
2. Make the minimum accurate edit.
3. Update frontmatter: `updated`, `sources`, `source_commit`, `confidence`.
4. Add supersession notes when correcting old claims.
5. Preserve and add relative links where useful.

Every claim follows SCHEMA `## Evidence`.

If creating a module page, use the module quality bar from the maintainer skill.

If ingest changes project status, architecture decisions, active work, next
tasks, blockers, or verification commands, update:

- `tracker`;
- `context` when onboarding facts, commands, risks, invariants, or
  read-first files changed;
- `handoff` when the next coding task, plan, blocker, git state, or
  verification state changed.

Keep `handoff` task-oriented. Its `Baton For Next Coding Agent` table
must keep start files, done criteria, and verification commands for each next
task.

## Step 6 - Update index and log

Update `index` for any page added, removed, renamed, or materially retitled.

Append one entry to `log` in SCHEMA `## Log format`, author `agent`, recording
the target, pages created and updated, notable changes, and follow-up.

## Step 7 - Report

Tell the user:

- what was ingested;
- pages created and updated;
- important findings;
- follow-up recommendations.

## Guardrails

- Never modify source code.
- Never delete pages during ingest; flag redundancy for lint.
- If more than half the wiki needs rewriting, stop and recommend a deliberate
  reorganization.
- Keep confidence honest.
