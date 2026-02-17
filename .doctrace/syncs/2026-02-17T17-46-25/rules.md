## Confidence
high

## Files read
- docs/rules.md - the doc being validated
- docs/architecture.md - related doc, verified command list and module structure
- docs/concepts.md - related doc, verified type definitions
- src/docsync/cli.py - entry point, verified actual CLI commands: validate, affected, preview, lock, init
- src/docsync/commands/affected.py - AffectedResult NamedTuple, data-first architecture with _build_output_data, --json flag
- src/docsync/commands/validate.py - ValidateResult/RefError as dataclasses, validate_refs iterator pattern
- src/docsync/commands/init.py - init command implementation
- src/docsync/commands/lock.py - lock command implementation
- src/docsync/commands/preview/tree.py - DependencyTree NamedTuple, tree logic lives inside preview module
- src/docsync/core/git.py - new module with FileChange/CommitInfo NamedTuples, git operations
- src/docsync/core/lock.py - Lock class, load/save functions
- src/docsync/core/parser.py - RefEntry/ParsedDoc NamedTuples, parse_doc
- src/docsync/core/config.py - Config/MetadataConfig classes, find_repo_root
- src/docsync/core/constants.py - shared constants and defaults

## Metadata updates
No metadata changes

## Changes made
- Line 47: changed `tree` to `preview` in the lowercase CLI commands list. The list read `validate`, `affected`, `tree`, `lock`, `init` but the actual CLI has no `tree` command; it is `preview`. The first command list on lines 8-12 already correctly listed `preview`.

## Why it was wrong
- The `tree` command was renamed/refactored into the `preview` command (commit f04e6fa: "refactor: preview command"). The tree functionality now lives inside `src/docsync/commands/preview/tree.py` as an internal module, but the CLI command is `preview`. The Lowercase CLI section on line 47 was not updated to reflect this change, while the command list at the top of the doc (lines 8-12) was already correct.
