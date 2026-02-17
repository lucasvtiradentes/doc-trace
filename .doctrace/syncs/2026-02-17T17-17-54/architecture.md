## Confidence
high

## Files read
- src/docsync/cli.py - verified subcommands (validate, affected, preview, lock, init), confirmed --json and --verbose flags exist, no --ordered flag
- src/docsync/commands/affected.py - verified AffectedResult has 6 fields (affected_docs, direct_hits, indirect_hits, circular_refs, matches, indirect_chains), get_changed_files is imported from core/git (not a private _get_changed_files), phases always shown, --json replaces --ordered
- src/docsync/core/git.py - verified get_changed_files, get_changed_files_detailed, get_merge_base, get_commits_in_range, get_tags_in_range, get_merged_branches_in_range functions
- src/docsync/core/lock.py - verified Lock class, load_lock, save_lock, find_lock; imports get_current_commit from core/git
- src/docsync/core/config.py - verified find_config traversal logic matches doc diagram
- src/docsync/core/parser.py - verified parse_doc, RefEntry, ParsedDoc types
- src/docsync/core/constants.py - verified DOCSYNC_DIR, CONFIG_FILENAME, LOCK_FILENAME constants
- src/docsync/commands/validate.py - verified validate_refs, ValidateResult match doc description
- src/docsync/commands/preview/__init__.py - verified preview module structure
- src/docsync/commands/init.py - verified init command
- src/docsync/commands/lock.py - verified lock subcommands (update, show)

## Changes made
- Fixed `_get_changed_files()` to `get_changed_files()` in affected command data flow diagram - function moved to core/git.py as a public function
- Updated AffectedResult fields from `(affected, direct, indirect, circular)` to `(affected, direct, indirect, circular, matches, indirect_chains)` to reflect two new fields added during refactor
- Replaced `--ordered` / `(by dep phases)` with `--json` / `(structured JSON)` in output diagram - --ordered was removed, phases are now always shown, and --json was added as the alternative output mode
- Updated default output label from `(hits grouped)` to `(hits + phases)` since phases are now always included

## Why it was wrong
- `_get_changed_files()` was renamed and moved: the git diff logic was extracted from affected.py into a new core/git.py module as a public function `get_changed_files()` (commit: "refactor: consolidate git operations into core/git.py")
- AffectedResult was extended with `matches` and `indirect_chains` fields during the data-first architecture refactor (commit: "feat: add git info to verbose, refactor to data-first architecture") to support verbose output showing which sources matched which docs and the chain of indirect propagation
- `--ordered` flag was removed and phases are now always displayed in output (commit: "feat: always show phases, add --json flag, remove --ordered"), replaced by `--json` for structured output
