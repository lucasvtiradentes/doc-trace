## Confidence
high

## Files read
- tests/affected/pure_logic/test_pure_logic.py - propagation, direct hits, find_affected_docs logic; mocks `get_changed_files`
- tests/affected/test_scope_resolution.py - resolve_commit_ref tests for --last, --since, --since-lock, --base-branch
- tests/affected/with_changes/test_with_changes.py - end-to-end affected with mocked changed files
- tests/affected/with_directory_ref/test_with_directory_ref.py - directory ref matching in affected
- tests/affected/build_indexes/test_build_indexes.py - index building from fixture docs
- tests/cli/test_affected_flags.py - CLI argument parsing for affected command (--last, --verbose, --json, --since)
- tests/preview/test_graph.py - graph data building and HTML generation
- tests/preview/test_search.py - doc search by keyword, case insensitivity, line numbers
- tests/preview/test_tree.py - dependency tree building, levels, circular detection
- docs/repo/tooling.md - pytest configuration reference
- docs/repo/cicd.md - CI test jobs reference

## Changes made
- Updated `tests/affected/` coverage description: added "scope resolution" (test_scope_resolution.py now tests resolve_commit_ref with --last, --since, --since-lock, --base-branch)
- Fixed mocked function name in "Mocked change detection" section: `_get_changed_files` changed to `get_changed_files` (no underscore prefix)

## Why it was wrong
- The `test_scope_resolution.py` file was modified (+17/-6) adding new tests for `--since` and `--base-branch` scope options, but the doc's description of `tests/affected/` did not mention scope resolution at all
- The function `_get_changed_files` was renamed to `get_changed_files` (visible in all three affected test files that mock it), making the doc's reference to the old name incorrect
