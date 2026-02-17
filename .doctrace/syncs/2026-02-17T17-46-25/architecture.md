## Confidence
high

## Files read
- src/docsync/cli.py - entry point; confirmed 5 subcommands (validate, affected, preview, lock, init), --json flag on affected, no --ordered flag
- src/docsync/commands/affected.py - AffectedResult has 6 fields (added matches, indirect_chains), _propagate returns 3 values, run() returns exit 2 on scope error, phases always shown, --json replaces --ordered
- src/docsync/commands/validate.py - validate_refs flow unchanged, confirmed diagram accuracy
- src/docsync/commands/preview/__init__.py - delegates to server.run, structure matches doc
- src/docsync/commands/lock.py - lock subcommands (update, show) unchanged
- src/docsync/commands/init.py - init command unchanged
- src/docsync/core/git.py - new module; get_changed_files(), get_changed_files_detailed(), FileChange, CommitInfo, get_merge_base(), get_commits_in_range(), get_tags_in_range(), get_merged_branches_in_range()
- src/docsync/core/lock.py - simplified, imports get_current_commit from core/git.py
- src/docsync/core/parser.py - RefEntry, ParsedDoc, parse_doc unchanged
- src/docsync/core/config.py - Config, MetadataConfig, find_config unchanged
- src/docsync/core/constants.py - constants unchanged
- docs/concepts.md - related doc, confirmed it exists and is relevant
- docs/features/affected.md - related doc, confirmed it exists
- docs/features/validation.md - related doc, confirmed it exists
- docs/features/preview.md - related doc, confirmed it exists

## Metadata updates
No metadata changes

## Changes made
- Fixed function name in affected data flow: `_get_changed_files()` -> `get_changed_files()` with note it lives in `core/git.py` (was refactored from private to public function in core/git module per commit aa94b0a)
- Updated _propagate output to include `indirect_chains` in both the data flow diagram and the BFS pseudocode output line
- Updated AffectedResult fields from `(affected, direct, indirect, circular)` to `(affected, direct, indirect, circular, matches, indirect_chains)` to match actual NamedTuple
- Replaced `--ordered` output branch with `--json` and changed label from "hits grouped" to "phases always shown" (per commit e9407ea which removed --ordered and added --json, making phases always visible)
- Added Exit 2 to observability table for scope errors in the affected command

## Why it was wrong
- `_get_changed_files()` was renamed to `get_changed_files()` and moved to `core/git.py` during the refactor in commit aa94b0a (consolidate git operations into core/git.py). The doc still referenced the old private function name.
- The `--ordered` flag was removed in commit e9407ea ("feat: always show phases, add --json flag, remove --ordered"). Phases are now always shown in the default output. The `--json` flag was added as the alternative output mode. The doc still showed the old --ordered branch.
- AffectedResult gained `matches` and `indirect_chains` fields as part of the data-first architecture refactor (commit b7fe847). The doc only listed the original 4 fields.
- The `_propagate()` function now returns `indirect_chains` as a third value (dict mapping indirect hit docs to the doc they were reached through), added during the same refactor. The pseudocode output line was outdated.
- Exit code 2 was present in `affected.run()` for scope errors but not documented in the observability table.
