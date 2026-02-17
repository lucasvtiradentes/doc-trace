## Confidence
high

## Files read
- docs/testing.md - the doc being validated
- docs/repo/tooling.md - related doc, pytest configuration reference
- docs/repo/cicd.md - related doc, CI test jobs reference
- tests/affected/pure_logic/test_pure_logic.py - propagation, direct hits, depth limits, circular detection
- tests/affected/test_scope_resolution.py - commit ref resolution (--last, --since, --since-lock, --base-branch)
- tests/affected/build_indexes/test_build_indexes.py - index building tests
- tests/affected/with_changes/test_with_changes.py - change detection integration
- tests/affected/with_directory_ref/test_with_directory_ref.py - directory ref matching
- tests/cli/test_affected_flags.py - CLI flag parsing including --json and --since flags
- tests/preview/test_tree.py - dependency tree building and level computation
- tests/preview/test_search.py - doc search functionality
- tests/preview/test_graph.py - graph data building and HTML generation

## Metadata updates
No metadata changes

## Changes made
- Updated `tests/affected/` coverage description: added "scope resolution" (was "index building, direct hits, propagation traversal, depth limits", now "index building, direct hits, propagation, depth limits, scope resolution")
- Fixed function name in "Mocked change detection" pattern: `_get_changed_files` changed to `get_changed_files` (underscore prefix removed)

## Why it was wrong
- The `tests/affected/test_scope_resolution.py` file was expanded from 6 tests to 9 tests (commits f04e6fa, e9407ea) adding `--since` flag tests and branch-based resolution. The doc's coverage description for `tests/affected/` did not mention scope resolution at all.
- The function `_get_changed_files` was renamed to `get_changed_files` (public API, no underscore prefix) as seen in all affected test files patching `docsync.commands.affected.get_changed_files`. The doc still referenced the old private name.
