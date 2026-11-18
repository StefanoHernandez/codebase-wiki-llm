---
type: Glossary
title: Glossary
description: Terms used in this wiki and in the plugin.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - canonical/codebase/default-schema.md
source_commit: 94f5dc0
confidence: high
---
# Glossary

| Term | Meaning |
| --- | --- |
| Canonical | the sources under `canonical/codebase/` that every package is generated from |
| Core map | the SCHEMA table that maps each core role to a path |
| Core read | what an agent reads at a new context: entry file, SCHEMA, index, context, handoff, tracker, risks, troubleshooting, glossary, last 10 log entries |
| Format version | the wiki structure version in SCHEMA `format_version`, separate from the release |
| Field-test wiki | the real adopted wiki used to test releases; its name is a private term |
| `upgrade:` line | validator output naming what a wiki still needs for the current format |
