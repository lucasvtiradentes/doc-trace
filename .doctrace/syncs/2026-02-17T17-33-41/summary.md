# Doc Sync Summary

Run: 2026-02-17T17-33-41
Reference: v0.1.1
Docs analyzed: 8

## Changes by doc

| Doc                       | Confidence | Changes          | Metadata        |
|---------------------------|------------|------------------|-----------------|
| docs/concepts.md          | high       | 1 content        | -               |
| docs/testing.md           | high       | 2 content        | -               |
| docs/features/preview.md  | high       | 4 content        | +1 source       |
| docs/repo/structure.md    | high       | 2 content        | -               |
| docs/features/affected.md | high       | 7 content        | +1 source       |
| docs/architecture.md      | high       | 3 content        | -               |
| docs/rules.md             | high       | 1 content        | -               |
| docs/overview.md          | high       | 1 content        | -               |

## All changes

### docs/concepts.md
- Added matches and indirect_chains fields to AffectedResult table

### docs/testing.md
- Updated tests/affected/ coverage description (added scope resolution)
- Fixed function name: _get_changed_files -> get_changed_files

### docs/features/preview.md
- Restructured Implementation table with Module column
- Added run() and build_dependency_tree() to Implementation table
- Removed get_file_history/get_file_at_commit (moved to core/git.py)
- Added source: src/docsync/core/git.py

### docs/repo/structure.md
- Added tests/preview/ to repository tree
- Added git.py to core/ module description

### docs/features/affected.md
- Replaced --show-changed-files with --verbose in usage
- Replaced --ordered with --json in usage
- Added --since v0.1.0 example
- Replaced --ordered section with --verbose and --json sections
- Updated default output example (phases always shown, indirect chain notation)
- Added --since to scope flag list
- Added source: src/docsync/core/git.py

### docs/architecture.md
- Changed preview.py to preview/ in entry point diagram
- Changed _get_changed_files() to get_changed_files()
- Replaced --ordered with --json, updated default output label

### docs/rules.md
- Changed tree to preview in Lowercase CLI command list

### docs/overview.md
- Updated version from 0.1.0 to 0.1.1

## Validation
- Status: passed
- Errors: none
