# Sync Report: docs/architecture.md

## Status: UPDATED

## Changes Made

### 1. Entry Point diagram - added missing commands
- **What**: Added `index` and `completion` commands to the entry point dispatcher diagram
- **Why**: `cli.py` now dispatches to 6 commands (info, affected, preview, init, index, completion), not 4. The `index` command was added in commit `0ebacd1` and `completion` in commit `a840728`.
- **Also fixed**: Changed `preview.py` to `preview/` in the diagram to match the actual package structure

### 2. Module Structure - added missing files
- **What**: Added `cmd_registry.py`, `commands/index.py`, `commands/completion.py`, and `core/filtering.py` to the module tree
- **Why**: These files were added in recent commits:
  - `cmd_registry.py` (commit `6daaede`): centralized command metadata
  - `commands/index.py` (commit `0ebacd1`): index generation from frontmatter
  - `commands/completion.py` (commit `a840728`): shell autocompletion
  - `core/filtering.py` (commit `706a305`): extracted fnmatch filter logic

### 3. Affected Data Flow - fixed function name and field name
- **What**: Changed `_build_indexes()` to `build_doc_index()` and `doc_to_docs` to `reverse_deps`
- **Why**: The `_build_indexes()` function no longer exists. The affected command now calls `build_doc_index()` from `core/docs.py`, which returns a `DocIndex` with a `reverse_deps` field (not `doc_to_docs`).

### 4. Affected Data Flow - removed depth_limit reference
- **What**: Removed `depth_limit` from the `_propagate()` annotation
- **Why**: The `_propagate()` function no longer accepts a `depth_limit` parameter (commit `20e5080` removed base command and related flags).

### 5. Propagation Algorithm - updated to match current implementation
- **What**: Removed `depth_limit` from Input, removed `depth_limit reached` check, removed inline circular ref recording, added `_find_circular_refs()` call after BFS loop
- **Why**: The `_propagate()` function was refactored. It no longer takes `depth_limit`, no longer tracks `depth`, and circular ref detection is now handled by a separate `_find_circular_refs()` function called after the BFS traversal completes.

## Not Changed (verified accurate)

- **Frontmatter sources**: `src/doctrace/cli.py`, `src/doctrace/commands/`, `src/doctrace/core/` are all still valid source paths
- **Frontmatter required_docs/related_docs**: All referenced docs exist and are still relevant
- **Data Flow - Info Command**: The `validate_refs()` flow is still accurate (function exists and works as described). The info command now also checks undeclared inline refs, but the diagram shows the core validation flow which is still correct.
- **Observability table**: Exit codes 0, 1, 2 are still accurate per source code
- **Config Loading pseudocode**: Still accurate per `config.py:find_config()` and `_walk_up_find()`

## Notes

- The Info Command data flow diagram is a simplification. The current `info.py:run()` also performs undeclared inline ref checking via `find_undeclared_inline_refs()`, which is not shown. This was not added since the existing diagram accurately describes the validation flow it claims to show.
- The AffectedResult in the Affected Data Flow diagram omits the `parsed_cache` field. This is a minor omission but the diagram focuses on conceptual flow, not exhaustive field listing.
