# Sync Report: docs/overview.md

**Date**: 2026-03-03T03-30-28
**Status**: UPDATED

## Sources Checked

- src/doctrace/cli.py
- src/doctrace/ (package directory)
- src/doctrace/cmd_registry.py (changed file in git context)
- pyproject.toml (for version verification)

## Related Docs Checked

- docs/architecture.md
- docs/concepts.md

## Changes Made

### 1. Version number updated (line 25)

- **Old**: `0.1.1`
- **New**: `0.2.3`
- **Reason**: pyproject.toml shows version is `0.2.3`. The doc was outdated.

## No Issues Found For

- **Commands table**: All 6 commands (info, affected, preview, init, index, completion) match `cmd_registry.py`. No `base` command was listed in the doc, so the removal of `base` from the codebase does not affect this doc.
- **`--since-base` flag**: Not mentioned anywhere in the doc. No change needed.
- **`--verbose` flag**: Not mentioned anywhere in the doc. No change needed.
- **Built With section**: All listed stdlib modules (argparse, pathlib, subprocess, fnmatch, json) are still used in the codebase.
- **Package Info table**: Name, Python version, entry point, and build system all match pyproject.toml.
- **What It Does section**: All three bullet points remain accurate per current source code.
- **Frontmatter sources**: Both `src/doctrace/cli.py` and `src/doctrace/` are valid paths. No change needed.
- **Frontmatter related_docs**: Both `docs/architecture.md` and `docs/concepts.md` exist. No change needed.

## Summary

| Metric | Count |
|--------|-------|
| Errors found | 1 |
| Fixes applied | 1 |
| Lines changed | 1 |
