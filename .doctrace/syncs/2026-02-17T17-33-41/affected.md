## Confidence
high

## Files read
- src/docsync/commands/affected.py - main affected command: run() signature shows --verbose, --json flags; --ordered removed; --since added; output always includes phases
- src/docsync/core/git.py - new file with get_changed_files_detailed, get_commits_in_range, get_tags_in_range, get_merged_branches_in_range used by --verbose
- src/docsync/cli.py - confirmed CLI flags: --since-lock, --last, --base-branch, --since, --verbose/-V, --json
- docs/concepts.md - related doc, AffectedResult type definition (already up to date)

## Metadata updates
- Added source: src/docsync/core/git.py (new file providing git diff/commit helpers used by affected command)

## Changes made
- Usage: replaced `--show-changed-files` with `--verbose` (flag was renamed in 3fb4765)
- Usage: replaced `--ordered` with `--json` (--ordered removed in e9407ea)
- Usage: added `--since v0.1.0` example (new flag from d8d3a36)
- Output Formats: removed `--ordered` section, replaced with `--verbose` and `--json` sections
- Output Formats: updated default output example to show phases (always shown now) and indirect hit `<-` notation
- How It Works: added `--since <ref>` to scope flag list
- Metadata: added src/docsync/core/git.py as related source

## Why it was wrong
- `--show-changed-files` was renamed to `--verbose` in commit 3fb4765, doc still referenced old flag name
- `--ordered` was removed in commit e9407ea, phases are now always shown in default output; doc still had a dedicated --ordered section
- `--since <ref>` flag was added in commit d8d3a36 but was missing from both usage examples and the scope flag documentation
- `--json` flag was added in commit e9407ea but was not documented
- `--verbose` now shows git context (changed files with line stats, commits, tags, merged branches, source-to-doc matches) but doc had no mention of this
- Indirect hits output format changed to show `<- via_doc` notation but doc showed old format without chain info
- src/docsync/core/git.py is a new file (commit b7fe847) heavily used by affected.py but was not listed as a related source
