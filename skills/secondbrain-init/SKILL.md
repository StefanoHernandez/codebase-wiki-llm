---
name: secondbrain-init
description: Bootstrap an adaptive personal and work knowledge vault.
---

<!-- Generated from secondbrain/workflows/secondbrain-init.md. Do not edit directly. -->

# /secondbrain-init

Bootstrap an adaptive SecondBrain vault.

Requires the SecondBrain maintainer skill. Follow `SCHEMA.md` if it exists;
otherwise use the default schema.

## Step 1 - Check preconditions

- If `index.md` and `SCHEMA.md` already exist, stop and ask whether to skip,
  extend the current vault, or run `/secondbrain-ingest` instead.
- If the current directory contains unrelated source code or project files,
  ask before creating a vault in place.

## Step 2 - Survey goals and existing material

Do a read-only survey. Do not deeply process every file yet.

Collect:

1. user-stated goals for the vault;
2. top-level files and directories;
3. existing `raw/`, `inbox/`, documents, notes, links, exports, meeting notes,
   expenses, and research material;
4. obvious domains needed: projects, work, personal, meetings, research,
   studies, tasks, expenses, areas, skills, people, publications;
5. sensitivity signals: personal, client, financial, legal, identity, health,
   or private meeting material.

## Step 3 - Propose adaptive structure

Tell the user:

- one sentence describing the intended vault;
- the core files/folders to create;
- which optional domains should be activated and why;
- which domains should remain inactive for now;
- any sensitive-data guardrails that matter for the detected material.

Ask: `Proceed with this SecondBrain structure? Adjust anything?`

Wait for confirmation before writing.

## Step 4 - Create scaffold

After confirmation:

1. Create the core: `index.md`, `SCHEMA.md`, `log.md`, `raw/`, `inbox/`,
   `archive/`.
2. Create only selected domain folders.
3. Adapt the schema and record active domains.
4. Create useful index sections for active domains.
5. Use explicit stubs only when they help navigation.

## Step 5 - Seed core pages

Create:

- `index.md` - vault catalog grouped by active domains;
- `SCHEMA.md` - active domains, frontmatter, sensitivity, and domain rules;
- `log.md` - vault change history.

If useful and supported by existing material, create initial domain index pages
such as `projects/index.md`, `research/index.md`, `meetings/index.md`, or
`tasks/index.md`.

## Step 6 - Report

Report:

- what was created;
- which domains are active;
- which material remains in `raw/` or `inbox/`;
- suggested next command, usually `/secondbrain-ingest <path>`.

## Guardrails

- Do not import all raw material during init.
- Do not create a large empty taxonomy.
- Do not infer personal meaning or sensitive classification beyond evidence.
- Do not write outside the current vault.
