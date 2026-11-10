# Index Template

Use this template for the `index` page (Core map). `index.md` is not a concept
page and takes no `type`; it is the map of the wiki and the place that says
which page owns each topic.

```markdown
---
title: <Project> wiki
generated: { by: <host>/<model>, at: <ISO 8601 UTC> }
sources:
  - <wiki-root>/SCHEMA.md
  - <wiki-root>/<Core map tracker path>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# <Project> wiki

<one paragraph: what this repository is and who works on it>

## Index

### Project
- [Work tracker](<tracker path>) — <description from the page>
- [Log](<log path>) — <description>
- [Decisions](<decisions path>) — <description>
- [Risks](<risks path>) — <description>

### <Topic group>
- [<Page title>](<path>) — <description>

### Cross-cutting
- [Schema](SCHEMA.md) · [agent context](<context path>) · [handoff](<handoff path>)
- [Troubleshooting](<troubleshooting path>) · [glossary](<glossary path>)

## Where things stand

Status lives only in the [tracker](<tracker path>), with the next steps; what
was done and when in the [log](<log path>).

## How this wiki is organised
<!-- wiki:owners -->

| Topic | Owner page |
| --- | --- |
| Activity status, next steps | [tracker](<tracker path>) |
| What was done, when | [log](<log path>) |
| Decisions and why | [decisions](<decisions path>) |
| Risks | [risks](<risks path>) |
| Next task for an agent | [handoff](<handoff path>) |
| Verified facts | [agent context](<context path>) |
```

Rules:

- **One topic, one page.** Each topic has exactly one owner page, listed in the
  `wiki:owners` table. Other pages link to it in one line and do not describe
  it again; a second description is a contradiction waiting to happen.
- `/wiki-init` writes the core rows and one row per confirmed topic.
  `/wiki-sync` and `/wiki-ingest` add a row when they create the owner page of
  a new topic, and update the row when a page is renamed or moved.
- Keep the `<!-- wiki:owners -->` marker on the line under the heading when the
  heading is translated. The table has two columns; the second cell links to
  the owner page. The validator checks both when the marker is present.
- Index entries reuse the page's `description:`; do not restate status here.
- Resolve every `<...>` path to the Core map path before writing.
