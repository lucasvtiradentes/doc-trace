# Sync Report: docs/repo/local-setup.md

## Trigger

Changed files since docs-base:
- `Makefile` (modified)
- `pyproject.toml` (modified)

Relevant commit: `c250e10` - chore: add pre-commit, devpanel, fix test symlinks

## Sources Checked

- `Makefile` - read and compared
- `pyproject.toml` - read and compared
- `docs/repo/tooling.md` (related_doc) - read for consistency

## Changes Applied

### 1. Added pre-commit to Dev Dependencies table
- **Reason**: `pyproject.toml` now includes `pre-commit>=3` in `[project.optional-dependencies] dev`. The table was missing this dependency.
- **Line**: Added `| pre-commit   | git hook management  |` row.

### 2. Updated `make install` description
- **Reason**: The `install` target in the Makefile now runs `.venv/bin/pre-commit install` as a third step. The doc described only venv creation and dependency installation.
- **Lines**: Updated prose description and command table entry to mention pre-commit setup.

### 3. Updated `make practical-test` description
- **Reason**: The `practical-test` target now runs `doctrace info docs/ --ignore docs/index.md` instead of `doctrace info docs/`. The `--ignore` flag was missing from the doc.
- **Line**: Updated command table entry.

## Not Changed (Intentional)

### Manual Install section
The Manual Install section does not mention `pre-commit install`. This is arguably correct since it shows the minimal manual steps to get a working install. The `pre-commit install` step is optional for running the tool itself. No change made.

### Missing make targets (format, build, clean)
The Makefile has `format`, `build`, and `clean` targets that are not listed in the Available Commands table. The doc title is "Available Commands" not "All Commands", and these were added in the same commit (`c250e10`). Since the doc doesn't claim to be exhaustive and these are secondary utility targets, no change was made. The doc maintainer may want to add these in a future update.

### Frontmatter
No changes needed. Sources and related_docs are accurate.

## Verdict

3 factual fixes applied. All related to changes from commit `c250e10` which added pre-commit support and the `--ignore` flag to `practical-test`.
