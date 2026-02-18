# Doc Sync Summary

Run: 2026-02-17T17-46-25
Reference: v0.1.1
Docs analyzed: 8

## Changes by doc

| Doc                       | Confidence | Changes              | Metadata         |
|---------------------------|------------|----------------------|------------------|
| docs/testing.md           | high       | 2 content            | -                |
| docs/concepts.md          | high       | 1 content            | +1 source        |
| docs/features/affected.md | high       | 4 content            | +2 sources       |
| docs/repo/structure.md    | high       | 2 content            | -                |
| docs/features/preview.md  | high       | 3 content            | +1 source        |
| docs/architecture.md      | high       | 3 content            | -                |
| docs/rules.md             | high       | 1 content            | -                |
| docs/overview.md          | high       | 2 content            | -                |

## All changes

### docs/testing.md
- Fixed `_get_changed_files` to `get_changed_files` (underscore prefix removed in refactor)
- Added "scope resolution" to `tests/affected/` coverage description

### docs/concepts.md
- Added 2 missing fields to AffectedResult: `matches` and `indirect_chains`
- Added source: src/docsync/core/git.py

### docs/features/affected.md
- Replaced --show-changed-files with --verbose in examples
- Removed --ordered, added --since and --json examples
- Rewrote Output Formats section (phases always shown, indirect chains)
- Added --since to scope flags list
- Added sources: src/docsync/core/git.py, src/docsync/cli.py

### docs/repo/structure.md
- Added `tests/preview/` to tree diagram
- Added `git.py` to core/ descriptions

### docs/features/preview.md
- Fixed "syntax highlighting" -> "marked.js" (no syntax highlighting library)
- Added bidirectional selection sync feature
- Fixed keyboard shortcuts description (left/right only, t/l for sidebar)
- Added source: src/docsync/core/git.py

### docs/architecture.md
- Fixed `_get_changed_files()` -> `get_changed_files() (core/git.py)`
- Updated AffectedResult fields (4 -> 6)
- Replaced --ordered with --json, added Exit 2 for scope errors

### docs/rules.md
- Fixed `tree` -> `preview` in lowercase CLI list

### docs/overview.md
- Updated version 0.1.0 -> 0.1.1
- Updated json description to include output handling

## Validation
- Status: passed
- Errors: none
