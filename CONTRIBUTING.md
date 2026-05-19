# Contributing

Thanks for considering a contribution.

## Ground rules

- The skill and the four commands share assumptions about frontmatter, log format, and decay rules. Keep them in sync.
- Skills go in `plugins/wiki-maintainer/skills/wiki-maintainer/`. Commands go in `plugins/wiki-maintainer/commands/`.
- Don't introduce hard-coded user paths (`~/.claude/...`, `/Users/...`). Reference the skill via the `Skill` tool's base-path header instead.
- Bump `version` in both `.claude-plugin/marketplace.json` and `plugins/wiki-maintainer/plugin.json` together. SemVer.
- Documentation goes in `README.md`; per-repo conventions go in the wiki's own `SCHEMA.md`, not here.

## Development loop

1. Clone the repo.
2. Symlink the plugin into your local Claude Code install for testing:
   ```bash
   ln -sf "$PWD/plugins/wiki-maintainer/skills/wiki-maintainer" ~/.claude/skills/
   for cmd in plugins/wiki-maintainer/commands/*.md; do
     ln -sf "$PWD/$cmd" ~/.claude/commands/
   done
   ```
   (Reverse with `rm` to clean up.)
3. Test the four commands against a small sample repo.
4. Open a PR.

## What to test

- `/wiki-init` on a repo with no `wiki/` directory — does it survey, propose, and ask before writing?
- `/wiki-ingest <path>` on a known file — does it update the index and log?
- `/wiki-sync` after a code change — does it touch only affected pages?
- `/wiki-lint` on a wiki with stale frontmatter — does it report instead of editing?

## Releasing

1. Update versions in both manifest files.
2. Update `CHANGELOG.md`.
3. Tag the release: `git tag v0.X.Y && git push --tags`.

## License

By contributing you agree your changes are released under the MIT license.
