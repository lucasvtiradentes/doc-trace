## Changes made
- Removed unsupported pytest version-matrix claim from tooling page.
- Reworded pytest and bump2version sections to match `pyproject.toml` and `Makefile` scope.

## Why it was wrong
- `pyproject.toml` defines pytest discovery options, but not a Python version matrix.
- `Makefile` provides local commands; CI matrix belongs to workflow files, not these listed sources.
