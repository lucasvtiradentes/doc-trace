# Sync Report: docs/repo/structure.md

## Flagged Sources
- `src/doctrace/commands/affected.py`
- `src/doctrace/core/config.py`

## Relevant Commits
- `20e5080` refactor: remove base command and --since-base flag
- `706a305` refactor: extract fnmatch filter to core/filtering.py

## Changes Applied

### 1. Removed "base state" from config.py description (line 32 in tree)
- **Before:** `config.py ← config loading/validation + base state`
- **After:** `config.py ← config loading/validation`
- **Reason:** The `Base` class, `save_config`, and `update_base` functions were removed from `config.py` in commit `20e5080`. The "base state" concept no longer exists in this module.

### 2. Added filtering.py to directory tree (between config.py and git.py)
- **Added:** `filtering.py ← fnmatch-based ignore filtering`
- **Reason:** `src/doctrace/core/filtering.py` was created in commit `706a305` (extracted from inline fnmatch logic). Both `affected.py` and `info.py` import `matches_ignore_pattern` from it.

### 3. Added filtering.py to "Key Directories > src/doctrace/core/" section
- **Added:** `filtering.py - fnmatch-based ignore filtering`
- **Reason:** Same as above. The Key Directories section lists all core modules and was missing this new one.

## Pre-existing Issues (not fixed)

These discrepancies exist but predate the flagged commit range and are outside scope:

- `src/doctrace/cmd_registry.py` not listed in the tree (added in commit `6daaede`, before range)
- `src/doctrace/commands/completion.py` not listed in the tree (added in commit `a840728`, before range)
- `src/doctrace/commands/index.py` not listed in the tree (added in commit `0ebacd1`, before range)
- `.github/workflows/update-docs.yml` not listed in the tree (pre-existing)
- `tests/core/` not listed under tests/ in the tree (pre-existing)

## Frontmatter

No changes needed. The `sources` list (`src/doctrace/`, `tests/`, `.github/workflows/`) uses directory-level references that still cover the new `filtering.py` file. Related docs (`docs/repo/tooling.md`, `docs/testing.md`) are still valid and exist.
