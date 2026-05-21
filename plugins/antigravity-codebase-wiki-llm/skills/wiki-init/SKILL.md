---
name: wiki-init
description: Bootstrap an engineering-first software project wiki under wiki/. Use when the user says /wiki-init, wiki init, bootstrap wiki, initialize codebase wiki, or asks to start a project wiki.
---

<!-- Generated from codebase/workflows/wiki-init.md. Do not edit directly. -->

# /wiki-init

Bootstrap the wiki for this repository. Run once per repo.

Requires the wiki maintainer skill. Follow `wiki/SCHEMA.md` if it exists;
otherwise use the default schema.

## Step 1 - Check preconditions

- If `wiki/index.md` already exists, stop and ask whether to skip, re-init, or
  run `/wiki-ingest` instead. Re-init requires explicit confirmation before
  deleting or replacing anything.
- If the current directory does not look like a code repo or software project,
  ask for confirmation before proceeding.

## Step 2 - Survey the repo

Do a read-only scan. Do not read every source file yet.

Collect:

1. top-level files and directories;
2. README and architecture/project docs;
3. package manifests and toolchain files;
4. main source directories and entrypoints;
5. tests, CI, build, lint, and deploy signals;
6. config/env/migration/runtime signals;
7. project docs, roadmap, status, proposal, or communication material;
8. existing agent/context/changelog files that should be migrated into
   `wiki/agent/` if in scope.

## Step 3 - Propose the plan

Tell the user:

- one sentence describing the project;
- which engineering pages will be populated;
- which modules/areas will get module pages;
- which project pages have enough evidence to populate;
- which project-docs pages will be stubs versus evidence-backed pages;
- any legacy docs proposed for later retirement;
- the initial agent context/activity/handoff pages that will be created.
- the portable project overview page name:
  `wiki/overview-<project-slug>.md`.

Ask: `Proceed with this plan? Adjust anything?`

Wait for confirmation before writing.

## Step 4 - Create the scaffold

After confirmation:

1. Create `wiki/` and the default directory tree.
2. Copy or adapt the default schema to `wiki/SCHEMA.md`.
3. Create pages with frontmatter: `title`, `updated`, `sources`,
   `source_commit` when git is available, and `confidence`.
4. Populate only what is supported by evidence. Use explicit stubs for pages
   that matter but have no verified content yet.

Create at least:

- `wiki/index.md`
- `wiki/log.md`
- `wiki/overview.md`
- `wiki/overview-<project-slug>.md`
- core `wiki/engineering/*` pages
- relevant `wiki/modules/*` pages
- `wiki/project/status.md` if any project-state evidence exists
- `wiki/agent/context.md`, `wiki/agent/activity.md`, `wiki/agent/handoff.md`
- `wiki/glossary.md`

## Step 5 - Write engineering pages first

Engineering is authoritative. Populate:

- architecture and data model from code/config/docs;
- development/testing from package scripts, test files, CI, and README;
- operations from deploy/runtime/config evidence;
- troubleshooting only from observed or documented failure modes;
- change-map with "if you need to change X, start here" guidance.

## Step 6 - Write module pages

For each selected module/area, write:

- purpose;
- key files;
- public interface;
- data/control flow;
- invariants;
- how to change this safely;
- verification;
- common failure modes;
- dependencies;
- related tests;
- open risks.

Omit unsupported sections rather than inventing.

## Step 7 - Write project and project-docs pages

Populate `project/` from evidence only. Link risks, requirements, milestones,
and decisions back to engineering pages.

Populate `project-docs/` as reusable communication material only when claims
are supported. Put unsupported but useful future claims in `project-docs/evidence.md`
as gaps or hypotheses.

Also create `wiki/overview-<project-slug>.md` as the portable project card. The
slug must be lowercase kebab-case. Include:

- what the project is;
- why it exists;
- current status;
- main stack or technical areas;
- milestones or next steps;
- important decisions to remember;
- links to the most relevant wiki pages;
- `## Personal Wiki Export`.

In `## Personal Wiki Export`, write content suitable for import into a
SecondBrain vault under `raw/projects/`. Include project name, short
description, current status, role in the user's work/life, personal motivation
if known, technologies or skills represented, important next steps, and
long-term notes. Do not invent personal meaning; use `Da confermare.` for
unknown personal context.

## Step 8 - Update index and log

Make `index.md` a complete catalog grouped by Overview, Engineering, Modules,
Project, Project Docs, Agent, and Reference.

Append to `log.md`:

```markdown
## [YYYY-MM-DD] init | bootstrapped wiki
- Scope: <one line>
- Pages created: <count>
- Modules: <list>
- Project/project-docs pages populated: <list or none>
- Portable overview: overview-<project-slug>.md
- Proposed for retirement: <list or none>
- Follow-up: run /wiki-lint to verify coverage
```

Append the initial entry to `wiki/agent/activity.md` with agent, trigger,
intent, actions, changed wiki files, validation, decisions, and follow-up.

## Step 9 - Report

Report:

- what was created;
- what was populated versus left as stubs;
- proposed legacy retirement;
- suggested next step: `/wiki-lint`.

## Guardrails

- Never modify source files during init.
- Never delete legacy docs during init.
- If the repo is huge, ask the user to narrow scope.
- Prefer fewer accurate pages over many generic pages.
