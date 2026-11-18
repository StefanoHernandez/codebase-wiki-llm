---
type: Decision
title: 0004 - Higher default size budgets
description: Default budgets: page 30 KB, core read 100 KB, log 30 KB.
status: accepted
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - CHANGELOG.md
  - canonical/codebase/default-schema.md
source_commit: 94f5dc0
confidence: high
---
# 0004 - Higher default size budgets

## Context
Measured on a real 91-page wiki: the core read was 112 KB against a 60 KB budget and eight pages sat between 16 and 20 KB.

## Decision
New SCHEMA defaults: single page 30 KB, core read 100 KB, log unchanged at 30 KB. Existing wikis keep their own `## Budgets`.

## Alternatives rejected
- Dropping troubleshooting and glossary from the core read: proposed, not chosen.
- Defining 1 KB as 1,024 bytes: proposed, not chosen.

## Consequences
Agents read more at a new context; existing wikis change only if edited by hand.

## Approval
<!-- wiki:approval -->
accepted: Stefano, conversation, 2026-11-18
