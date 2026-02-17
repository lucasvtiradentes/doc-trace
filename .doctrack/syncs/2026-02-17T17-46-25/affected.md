## Confidence
high

## Files read
- src/docsync/commands/affected.py - main implementation; found new --since flag, --verbose/--json flags, data-first architecture with _build_output_data and _print_from_data, phases always shown
- src/docsync/cli.py - CLI argument definitions; confirmed --verbose/-V, --json, --since flags exist; --show-changed-files and --ordered removed
- src/docsync/core/git.py - git helpers; FileChange, get_changed_files_detailed, get_commits_in_range, get_tags_in_range, get_merged_branches_in_range used by verbose mode
- docs/concepts.md - related doc; AffectedResult type definition (already includes indirect_chains field)

## Metadata updates
- Added source: src/docsync/core/git.py (heavily used by affected command for verbose mode git data)
- Added source: src/docsync/cli.py (defines CLI flags for affected command)

## Changes made
- Replaced --show-changed-files with --verbose in usage examples (flag was renamed in commit 3fb4765)
- Removed --ordered from usage examples (flag was removed in commit e9407ea)
- Added --since and --json usage examples (added in commits d8d3a36 and e9407ea)
- Rewrote "Output Formats" section: default output now always includes phases and shows indirect hit chains; replaced --ordered section with --verbose and --json sections
- Added --since <ref> to Step 1 scope flag list (added in commit d8d3a36)
- Added src/docsync/core/git.py and src/docsync/cli.py to related sources metadata

## Why it was wrong
- The --show-changed-files flag was replaced by --verbose in commit 3fb4765, but the doc still referenced the old flag name
- The --ordered flag was removed in commit e9407ea (phases are now always shown), but the doc had a dedicated section for it and a usage example
- The --since flag (commit d8d3a36) and --json flag (commit e9407ea) were added but never documented
- The default output format changed: phases are always displayed, and indirect hits now show the propagation chain (e.g., "docs/overview.md <- docs/api.md"); the doc showed the old format without phases or chains
- The doc only listed src/docsync/commands/affected.py as a source, but the affected command heavily depends on src/docsync/core/git.py for verbose mode data and src/docsync/cli.py for flag definitions
