---
name: codebase-wiki-context
description: Use a repository-local wiki as project context in Codex. Use when working in a repo that has wiki/index.md, when the user asks about project context, or when a task should account for existing wiki knowledge.
---

# Codebase Wiki Context

When a repository has `wiki/index.md`, treat it as durable project context.

## Start of relevant work

Read `wiki/index.md` early when:
- The user asks about architecture, modules, roadmap, or onboarding.
- A coding task could be affected by existing project conventions.
- The user asks to continue previous work and the wiki exists.

Read only the linked wiki pages needed for the task. Prefer wiki context before a
broad source scan, then verify against source when correctness matters.

## During work

- If the wiki covers the topic, use it to orient the source inspection.
- If source code contradicts the wiki, trust source code and flag the wiki drift.
- If the task modifies source files and the repo has a wiki, run or recommend
  `/wiki-sync` at the end depending on scope and user intent.

## Boundaries

This skill does not create a wiki. Use `/wiki-init` for that.
