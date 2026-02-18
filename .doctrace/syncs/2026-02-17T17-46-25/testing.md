## Confidence
high

## Files read
- docs/testing.md - the doc being validated
- tests/affected/pure_logic/test_pure_logic.py - tests for direct hits, propagation, depth limits; patches `get_changed_files` (no underscore prefix)
- tests/affected/test_scope_resolution.py - tests for `resolve_commit_ref` with --last, --since-lock, --base-branch, --since flags
- tests/affected/with_changes/test_with_changes.py - integration test patching `get_changed_files`
- tests/affected/with_directory_ref/test_with_directory_ref.py - directory ref matching test patching `get_changed_files`
- tests/affected/build_indexes/test_build_indexes.py - index building test
- tests/cli/test_affected_flags.py - CLI flag tests including --json and --since
- tests/preview/__init__.py - empty init file
- tests/preview/test_graph.py - graph data building and HTML generation tests
- tests/preview/test_search.py - doc search tests
- tests/preview/test_tree.py - dependency tree and level computation tests
- pyproject.toml - pytest config verification
- Makefile - CI command verification
- docs/repo/tooling.md - verified exists (related doc)
- docs/repo/cicd.md - verified exists (related doc)

## Metadata updates
No metadata changes

## Changes made
- Fixed `_get_changed_files` to `get_changed_files` in "Mocked change detection" section (underscore prefix was removed in refactor)
- Added "scope resolution" to `tests/affected/` coverage description (new `test_scope_resolution.py` tests --last, --since-lock, --base-branch, --since)

## Why it was wrong
- `_get_changed_files` was renamed to `get_changed_files` (public function) during the data-first architecture refactor (commit b7fe847). All test files now patch `docsync.commands.affected.get_changed_files` without the underscore prefix.
- `tests/affected/test_scope_resolution.py` was significantly expanded (from 6 to 17 lines added) to cover `--since` and `--base-branch` scope options. The doc's coverage description for `tests/affected/` did not mention scope resolution at all.
