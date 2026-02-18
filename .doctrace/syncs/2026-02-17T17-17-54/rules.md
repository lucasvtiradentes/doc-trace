## Confidence
high

## Files read
- src/docsync/cli.py - confirmed registered commands: validate, affected, preview, lock, init (no tree)
- src/docsync/commands/affected.py - AffectedResult NamedTuple, new git data integration with FileChange/CommitInfo
- src/docsync/commands/validate.py - ValidateResult and RefError are dataclasses, not NamedTuples
- src/docsync/commands/lock.py - lock update/show subcommands
- src/docsync/commands/init.py - init command
- src/docsync/commands/preview/ - preview module directory (replaced standalone tree command)
- src/docsync/commands/preview/tree.py - DependencyTree NamedTuple still exists but is internal to preview
- src/docsync/core/git.py - new module with FileChange and CommitInfo NamedTuples
- src/docsync/core/lock.py - Lock class, load/save functions
- src/docsync/core/parser.py - RefEntry and ParsedDoc NamedTuples
- src/docsync/core/config.py - Config and MetadataConfig classes
- docs/architecture.md - related doc, confirmed tree removal
- docs/concepts.md - related doc, type definitions

## Changes made
- Line 47: replaced `tree` with `preview` in lowercase CLI commands list
- Lines 56-59: replaced `DependencyTree` with `FileChange` and `CommitInfo` in the NamedTuple examples list

## Why it was wrong
- The `tree` command was removed (commit: "refactor: remove tree command") and replaced by the `preview` command. The CLI commands list on line 47 still referenced `tree` instead of `preview`.
- `DependencyTree` moved from a top-level command return type to an internal type inside `commands/preview/tree.py`. Meanwhile, `core/git.py` was added with two new NamedTuples (`FileChange`, `CommitInfo`) that are used as return types in the affected command's data pipeline. The NamedTuple examples list was outdated.
