## Confidence
high

## Files read
- docs/rules.md - the doc under validation
- docs/architecture.md - related doc, verified command list and module structure
- docs/concepts.md - related doc, verified type definitions
- src/docsync/cli.py - confirmed registered commands: validate, affected, preview, lock, init (no tree)
- src/docsync/commands/affected.py - verified AffectedResult NamedTuple, propagation logic
- src/docsync/commands/validate.py - verified ValidateResult/RefError are dataclasses, validate_refs yields results
- src/docsync/commands/preview/__init__.py - confirmed preview module exists
- src/docsync/commands/preview/tree.py - confirmed DependencyTree NamedTuple moved here from commands/tree.py
- src/docsync/core/git.py - new module with git operations (FileChange, CommitInfo, get_changed_files, etc.)
- src/docsync/core/lock.py - verified Lock class, imports get_current_commit from core/git
- src/docsync/core/parser.py - verified RefEntry, ParsedDoc NamedTuples

## Metadata updates
No metadata changes

## Changes made
- Line 47: replaced `tree` with `preview` in the Lowercase CLI command list (`validate`, `affected`, `tree`, `lock`, `init` -> `validate`, `affected`, `preview`, `lock`, `init`)

## Why it was wrong
- The `tree` command was removed in commit e2e746b ("refactor: remove tree command") and its functionality was absorbed into the `preview` module (src/docsync/commands/preview/tree.py). The CLI (src/docsync/cli.py) registers `preview` as the subcommand, not `tree`. The doc's Lowercase CLI section still listed `tree` as a valid command.
