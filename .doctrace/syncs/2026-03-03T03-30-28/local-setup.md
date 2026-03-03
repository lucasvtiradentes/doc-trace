# Sync Report: docs/repo/local-setup.md

## Trigger

Source files changed since `docs-base`:
- `Makefile` (renamed "fix" to "format", added pre-commit install to install target, added build/clean targets, added .PHONY)
- `pyproject.toml` (added pre-commit to dev deps)

Commit: c250e10 chore: add pre-commit, devpanel, fix test symlinks

## Changes Applied

### 1. Added `pre-commit` to Dev Dependencies table
- **Reason**: `pre-commit>=3` was added to `[project.optional-dependencies] dev` in `pyproject.toml`. The table was missing this dependency.
- **Source**: `pyproject.toml` line 13

### 2. Updated `make install` description
- **Reason**: The `install` Makefile target now runs `.venv/bin/pre-commit install` in addition to creating the venv and installing deps. The doc's description ("creates .venv/ and installs package with dev dependencies") was incomplete.
- **Source**: `Makefile` lines 1-4
- **Before**: "This creates `.venv/` and installs package with dev dependencies."
- **After**: "This creates `.venv/`, installs package with dev dependencies, and sets up pre-commit hooks."

### 3. Added `make format` to Available Commands table
- **Reason**: The `fix` target was renamed to `format` in the Makefile. The doc never listed `make fix`, but `make format` is a key development command (ruff fix + format) that pairs with `make check`.
- **Source**: `Makefile` lines 10-12

### 4. Updated `make practical-test` description
- **Reason**: The Makefile target now runs `doctrace info docs/ --ignore docs/index.md` but the doc said `doctrace info docs/`.
- **Source**: `Makefile` line 18
- **Before**: `doctrace info docs/`
- **After**: `doctrace info docs/ --ignore docs/index.md`

### 5. Added `make build` and `make clean` to Available Commands table
- **Reason**: These are new Makefile targets added in the same commit. The commands table now reflects all available targets.
- **Source**: `Makefile` lines 26-31

## No Change Needed

- **Frontmatter sources**: Still correct (`Makefile`, `pyproject.toml`). The new `.pre-commit-config.yaml` file is not referenced in detail by this doc, so it does not need to be added as a source.
- **Frontmatter related_docs**: `docs/repo/tooling.md` is still relevant.
- **Manual Install section**: Still accurate for manual setup (pre-commit install is a make-only convenience).
- **Running Commands section**: No changes to CLI commands themselves.
- **Requirements section**: No changes needed.
