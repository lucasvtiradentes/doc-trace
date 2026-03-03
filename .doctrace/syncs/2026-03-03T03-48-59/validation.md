# Sync Report: docs/features/validation.md

## Status: UPDATED

## Changes Made

### 1. Error Output section -- fixed output format
- **What changed**: The `Error Output` section showed the old `Warnings (N):` format with `file:line: message` lines. The actual output now uses dedicated section headers (e.g., `## Missing Referenced Docs`) with `doc -> ref (type)` format, as implemented in `_print_from_data()`.
- **Why**: Output format was overhauled in commit `511478d` (refactor: align output format with shell script).
- **Lines affected**: 53-63

### 2. Exit Codes section -- broadened exit code 1 description
- **What changed**: Exit code 1 description changed from "one or more refs invalid" to "errors found (missing refs, circular deps, or undeclared inline refs)".
- **Why**: The `run()` function (info.py line 265) now returns 1 for `tree.circular or errors or undeclared_inline`, not just missing refs. Undeclared inline refs were added in commit `2cac932`, circular deps were already checked but not documented.
- **Lines affected**: 70

### 3. Output Format section -- updated to match new structured report
- **What changed**: Replaced the simplified `Level N:` / `Warnings` format with the actual structured report format including banner, section headers, `(req: N, rel: N)` counts per doc, and summary section.
- **Why**: The output was restructured in commit `511478d` to use `_print_from_data()` which produces a multi-section report with `=`/`-` separators, doc counts, and a summary block.
- **Lines affected**: 72-98

### 4. Behavior bullet -- fixed incorrect config field name
- **What changed**: Changed "Skips docs matching ignored_paths patterns" to "Skips docs matching ignore_inline_refs config patterns and --ignore CLI patterns".
- **Why**: There is no `ignored_paths` field in the codebase. The actual mechanism uses `config.ignore_inline_refs` (from doctrace.json) combined with `--ignore` CLI flag patterns, both fed to `matches_ignore_pattern()` from `core/filtering.py`. Added in commit `d7935cc`.
- **Lines affected**: 103

### 5. Behavior bullet -- fixed parse error handling description
- **What changed**: Changed "Reports docs that fail to parse as validation errors (continues scanning)" to "Silently skips docs that fail to parse (continues scanning)".
- **Why**: In `build_doc_index()` (docs.py lines 127-129), parse failures (OSError, UnicodeDecodeError, ValueError) are caught and silently skipped via `continue`. Failed docs never enter `parsed_cache` and are never reported.
- **Lines affected**: 104

## Not Changed (intentionally kept as-is)

- **Frontmatter metadata**: All sources and required_docs references are accurate and exist.
- **Description**: "Validates that all doc references point to existing files" is accurate for the validation aspect, though the `info` command now also checks inline refs and circular deps. Left as-is since it's not misleading for this doc's scope.
- **What It Checks sections**: Required Docs, Related Docs, and Sources checks are all accurately described and match the source code.
- **Implementation Details table**: All four listed functions exist and descriptions match. New functions added in recent commits (e.g., `extract_inline_refs`, `find_undeclared_inline_refs`, `_build_data`, `_print_from_data`) were not added per the "never expand" rule.
- **Usage section**: `doctrace info docs/` is correct per cli.py.

## Sources Reviewed

- src/doctrace/commands/info.py (validation implementation, output formatting)
- src/doctrace/core/docs.py (metadata extraction, dependency tree building)
- src/doctrace/core/filtering.py (ignore pattern matching)
- src/doctrace/core/config.py (Config fields, ignore_inline_refs)
- src/doctrace/cli.py (CLI argument parsing)
- docs/concepts.md (Phase 1 dependency, already updated)
- docs/overview.md (Phase 1 dependency, already updated)
