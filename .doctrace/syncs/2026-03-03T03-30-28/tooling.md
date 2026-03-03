# Sync Report: docs/repo/tooling.md

**Date:** 2026-03-03
**Status:** ok
**Changes applied:** 0

## Sources checked

- `pyproject.toml` - verified all tool configs (ruff, pytest, hatch, towncrier, bump2version)
- `Makefile` - verified targets and commands
- `.pre-commit-config.yaml` - new file, not referenced in doc

## Findings

### No factual errors found

All documented tool configurations (ruff settings, pytest options, hatch build targets, towncrier settings, bump2version usage) match the current source code exactly.

### Observations (no changes made)

1. **Makefile `fix` renamed to `format`**: The doc does not reference any `make` targets (it only shows direct tool commands like `ruff check .`, `pytest -v`, etc.), so the rename from `make fix` to `make format` does not create a factual error in this doc.

2. **pre-commit not documented**: `.pre-commit-config.yaml` was added with ruff hooks, and `pre-commit>=3` was added to dev dependencies in `pyproject.toml`. The doc does not mention pre-commit. This is a gap in coverage but not a factual error in existing content. Per conservative editing rules, no content was added. Consider adding a pre-commit section in a future intentional doc update, and adding `.pre-commit-config.yaml` to the frontmatter `sources` at that time.

3. **Makefile `build` and `clean` targets added**: The doc does not document Makefile targets, so these additions do not affect accuracy.
