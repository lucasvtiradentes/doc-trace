## Confidence
high

## Files read
- src/docsync/core/git.py - new module (228 lines) consolidating all git operations: diff, log, merge-base, file history, commit range queries
- src/docsync/commands/preview/ - confirmed existing files: __init__.py, server.py, tree.py, graph.py, search.py, template.html
- tests/ - confirmed directories: affected, validate, config, parser, preview, cli (no tree/ directory)
- docs/repo/tooling.md - related doc, no issues
- docs/testing.md - related doc, already lists tests/preview/

## Changes made
- Added `tests/preview/` entry to the tree structure diagram (was missing despite directory existing with test_graph.py, test_search.py, test_tree.py)
- Added `git.py` to the "Key Directories > src/docsync/core/" bullet list with description "git operations (diff, log, merge-base)"

## Why it was wrong
- `tests/preview/` was missing from the tree diagram because it was added as part of the "refactor: preview command" commit that created `src/docsync/commands/preview/` as a new directory. The tree structure in the doc had the preview source files but not the corresponding test directory.
- `core/git.py` was missing from the Key Directories section because it was introduced in the "refactor: consolidate git operations into core/git.py" commit after the doc was last updated. The tree diagram already had `git.py` listed (line 26) but the descriptive bullet list in the "src/docsync/core/" section did not include it.
