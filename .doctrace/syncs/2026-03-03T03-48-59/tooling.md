# Sync Report: docs/repo/tooling.md

## Sources Reviewed
- pyproject.toml
- Makefile

## Changes Applied
None. All existing documentation content is factually accurate against the current source code.

## Notes
- **pre-commit added but not documented**: The commit `c250e10` added `pre-commit>=3` to dev dependencies in `pyproject.toml` and added `.venv/bin/pre-commit install` to the Makefile `install` target. The doc does not mention pre-commit. This is new tooling not yet covered in the doc, but since the existing content is not incorrect (it just does not cover this new tool), no changes were made per conservative editing rules (rule 6: never expand).
- All Ruff settings (line-length=120, select=E,F,I) match `pyproject.toml`.
- Pytest config (testpaths, python_files) matches `pyproject.toml`.
- Hatch build config matches `pyproject.toml`.
- Towncrier settings and fragment types match `pyproject.toml`.
- Bump2version is still listed in dev dependencies, doc is accurate.

## Recommendations
- Consider adding a "Pre-commit" section documenting the pre-commit hook setup, since it is now part of the standard dev workflow via `make install`.
