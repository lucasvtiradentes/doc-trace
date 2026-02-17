## Confidence
high

## Files read
- src/docsync/cli.py - confirmed 5 subcommands (validate, affected, preview, lock, init), no --ordered flag, --json flag present
- src/docsync/commands/affected.py - get_changed_files() imported from core/git.py (not private _get_changed_files), --ordered removed, phases always shown, --json added
- src/docsync/commands/preview/__init__.py - preview is a package, not a single .py file
- src/docsync/commands/preview/server.py - confirmed run() entry point
- src/docsync/core/git.py - confirmed get_changed_files() is the public function name
- src/docsync/core/config.py - find_config() matches doc's Config Loading section
- src/docsync/core/parser.py - parse_doc(), RefEntry, ParsedDoc match doc
- src/docsync/core/lock.py - Lock class matches doc
- src/docsync/core/constants.py - constants match doc
- docs/concepts.md - related doc, exists and relevant
- docs/features/affected.md - related doc, exists and relevant
- docs/features/validation.md - related doc, exists and relevant
- docs/features/preview.md - related doc, exists and relevant

## Metadata updates
No metadata changes

## Changes made
- Line 19: changed `preview.py` to `preview/` in entry point diagram (preview is now a package)
- Line 64: changed `_get_changed_files()` to `get_changed_files()` (function moved to core/git.py as public API)
- Lines 91-92: replaced `--ordered (by dep phases)` with `--json (full JSON output)` and updated default output label to `(hits + phases)` since phases are always shown now

## Why it was wrong
- preview.py -> preview/: commit f04e6fa refactored preview into a package with server.py, graph.py, tree.py, search.py submodules. The entry point diagram still referenced the old single-file path.
- _get_changed_files() -> get_changed_files(): commit aa94b0a consolidated git operations into core/git.py. The function is now a public function in that module, not a private helper in affected.py.
- --ordered -> --json: commit e9407ea removed the --ordered flag and made phases always visible in default output. It also added --json as the new alternative output format. The diagram still showed the removed --ordered flag.
