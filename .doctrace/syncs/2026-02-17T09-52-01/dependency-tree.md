## Changes made
- Corrected circular-dependency behavior details.
- Added implementation notes about skipped parse failures and filtering to existing `related docs` paths.

## Why it was wrong
- `src/docsync/commands/tree.py::_compute_levels` does not assign both docs in a cycle to level 0; levels can differ based on traversal.
- `src/docsync/commands/tree.py::_build_doc_dependencies` skips docs that fail `parse_doc(...)` and only records dependencies when `repo_root / ref.path` exists.
