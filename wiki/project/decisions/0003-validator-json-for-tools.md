---
type: Decision
title: 0003 - Validator JSON output for tools
description: `validate-wiki.py --json` is the interface for tools such as the desktop app.
status: accepted
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - CHANGELOG.md
  - canonical/codebase/scripts/validate-wiki.py
source_commit: 94f5dc0
confidence: high
---
# 0003 - Validator JSON output for tools

## Context
The desktop app and other tools need findings, `upgrade:` and `info:` lines in a form they can parse.

## Decision
`validate-wiki.py --json <wiki-root>` prints one JSON document with the validator and format versions, exit code and the lists; the text output stays for people.

## Alternatives rejected
- Reasons not recorded.

## Consequences
A change to the JSON shape is a change for the app, which bundles a copy of the validator.

## Approval
<!-- wiki:approval -->
accepted: Stefano, release v0.13.0 and CHANGELOG 0.13.0, 2026-11-11
