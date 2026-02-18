## Confidence
high

## Files read
- src/docsync/commands/affected.py - full affected command: resolve_commit_ref (now has --since), run() (now has --verbose and --json flags, no --ordered), data-first architecture with _build_output_data/_print_from_data
- src/docsync/core/git.py - new module extracted for git operations: get_changed_files, get_changed_files_detailed (FileChange with status/lines), get_commits_in_range, get_tags_in_range, get_merged_branches_in_range, get_merge_base
- src/docsync/cli.py - CLI argument definitions confirming --since, --verbose/-V, --json flags and removal of --ordered and --show-changed-files
- docs/concepts.md - related doc listing AffectedResult type (already up to date with matches and indirect_chains fields)

## Changes made
- Replaced `--show-changed-files` usage example with `--verbose` and added `--json` and `--since` examples
- Replaced `--ordered` output section with `--verbose / -V` and `--json` sections; phases are now always shown in default output
- Updated default output example to show indirect hit chain format (`<- docs/api.md`) and phases section
- Added `--since <ref>` to the scope flag list in "Step 1: Get Changed Files"
- Extended implementation diagram to show _build_output_data() and the two output paths (_print_from_data for text, json.dumps for --json)
- Added src/docsync/core/git.py to related sources metadata

## Why it was wrong
- `--show-changed-files` was replaced by `--verbose` (commit: feat: replace --show-changed-files with --verbose flag) - the old flag no longer exists in CLI or run() signature
- `--ordered` was removed (commit: feat: always show phases, add --json flag, remove --ordered) - phases now always appear in output, there is no separate flag for them
- `--since <ref>` flag was added (commit: feat: add --since flag for arbitrary git ref) but was not documented anywhere in the doc
- `--json` flag was added (commit: feat: always show phases, add --json flag, remove --ordered) but was not documented
- `--verbose` shows git context (changed files with status/line stats, commits, tags, merged branches, source-to-doc matches) which was not documented
- The output format changed: indirect hits now show chain info (`<- via_doc`), phases always appear. The old example only showed direct/indirect lists without phases
- The implementation diagram stopped at AffectedResult but the data-first refactor (commit: feat: add git info to verbose, refactor to data-first architecture) added _build_output_data and _print_from_data as the rendering pipeline
- src/docsync/core/git.py is a new module (228 lines) that the affected command depends on heavily but was missing from related sources
