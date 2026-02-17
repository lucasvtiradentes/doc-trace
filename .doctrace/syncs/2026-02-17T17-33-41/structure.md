## Confidence
high

## Files read
- docs/repo/structure.md - the doc being validated
- docs/repo/tooling.md - related doc, verified it exists and is relevant
- docs/testing.md - related doc, verified it exists; confirmed tests/preview/ listed there
- src/docsync/commands/ (directory listing) - verified command files match doc tree
- src/docsync/core/ (directory listing) - found git.py missing from doc
- src/docsync/commands/preview/ (directory listing) - verified preview submodule matches doc
- tests/ (directory listing) - found tests/preview/ missing from doc
- .github/workflows/ (glob) - verified workflow files match doc

## Metadata updates
No metadata changes

## Changes made
- Added `tests/preview/` to the repository tree under tests/ (was missing)
- Added `git.py` to the core/ module listing in the Key Directories section with description "git operations (diff, log, changed files)"

## Why it was wrong
- `tests/preview/` was added by commits f04e6fa and e2e746b which refactored the preview command and removed the old tree command. The old `tests/tree/` directory was deleted and replaced by `tests/preview/` containing test_graph.py, test_search.py, and test_tree.py. The doc's tree never included this new test directory.
- `core/git.py` was added by commit aa94b0a "refactor: consolidate git operations into core/git.py" (+228 lines). This new module provides git diff, log, and changed file operations used across commands. The doc's tree already showed `git.py` in the core/ directory listing (line 26) but the Key Directories description section for core/ did not mention it.
