# Sync Report: docs/guides/create-release.md

## Result: NO_CHANGES

## Sources Checked
- .github/workflows/release.yml
- .changelog/
- pyproject.toml
- .bumpversion.cfg
- Makefile (not in frontmatter, but referenced via `make changelog-draft`)

## Related Docs Checked
- docs/repo/cicd.md

## Changed Files Evaluated
- **Makefile**: Renamed `fix` target to `format`, added `pre-commit install` to `install`, added `build` and `clean` targets, added `.PHONY`. This doc does not reference `make fix`, `make install`, `make build`, `make clean`, or `make format`, so no impact. The `make changelog-draft` target used by this doc is unchanged.
- **pyproject.toml**: Added `pre-commit` to dev deps. This doc does not reference the dev dependency list, so no impact. The towncrier config, version, and project metadata referenced by this doc are unchanged.

## Findings

All content in the doc is accurate against current source code:

1. **Tools** (towncrier, bump2version) - confirmed in pyproject.toml dev deps and release.yml
2. **Changelog fragment format** (`.changelog/+<name>.<type>.md`) - confirmed by actual files in `.changelog/`
3. **Fragment types** (feature, bugfix, misc) - matches pyproject.toml `[tool.towncrier]` config exactly
4. **Release flow diagram** - matches release.yml workflow steps
5. **`make changelog-draft` command** - target exists and is unchanged in Makefile
6. **Manual trigger instructions** - matches workflow_dispatch config in release.yml

## Notes

- The Makefile is not listed in the frontmatter `sources:` but the doc references `make changelog-draft` on line 71. This is a minor traceability gap but not a factual error. No change made per conservative editing rules.
