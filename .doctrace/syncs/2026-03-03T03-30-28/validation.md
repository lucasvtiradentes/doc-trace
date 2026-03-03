# Sync Report: docs/features/validation.md

## Status: UPDATED

## Changes Applied

### 1. Frontmatter: added new sources
- **What**: Added `src/doctrace/cli.py`, `src/doctrace/core/config.py`, and `src/doctrace/core/filtering.py` to frontmatter `sources:`
- **Why**: These files now contain logic documented by this page (`--ignore` flag, `ignore_inline_refs` config key, ignore pattern matching). Without them, the doc would not be flagged when those files change.

### 2. Description: "phases" changed to "levels"
- **What**: Line "shows dependency phases" changed to "shows dependency levels"
- **Why**: The source code uses `levels` (see `_build_data` key `"levels"`, `_print_from_data` header `"Documentation Levels"`). The term "phases" does not appear in the codebase.

### 3. Usage: added --ignore flag example
- **What**: Added `doctrace info docs/ --ignore "docs/drafts/*"` usage line
- **Why**: The `--ignore` flag was added to the `info` subparser in `cli.py` (line 21) and is passed to `info.run()` (line 52). Omitting it is a factual gap.

### 4. What It Checks: added "Undeclared Inline Refs" subsection
- **What**: Added new subsection documenting the inline ref validation check
- **Why**: `find_undeclared_inline_refs()` (info.py lines 88-103) is a new validation check. The "What It Checks" section claims to enumerate all checks, so omitting this is factually incomplete.

### 5. Error Output: updated format
- **What**: Changed from `Warnings (2):` format to sectioned `## Missing Referenced Docs` / `ERROR:` format
- **Why**: `_print_from_data()` (info.py lines 166-216) uses `_print_section_header` with `## title` and `"-" * 40`, and prints `ERROR:` prefix. The old "Warnings" format no longer exists in the code.

### 6. Exit Codes: updated meaning for code 1
- **What**: Changed from "one or more refs invalid" to "circular deps, missing refs, or undeclared inline refs found"
- **Why**: `run()` (info.py line 265) sets `has_errors = tree.circular or errors or undeclared_inline`. Exit code 1 now covers three distinct error categories.

### 7. Output Format: updated example to match new format
- **What**: Replaced old `Level 0:` / `Warnings (1):` example with new sectioned format including `(req: N, rel: N)` annotations and summary section
- **Why**: `_print_from_data()` outputs docs with required/related counts per doc, uses section headers, and includes a summary block. The old format is no longer produced by the code.

### 8. Behavior: fixed "ignored_paths" reference
- **What**: Changed "Skips docs matching ignored_paths patterns" to "Skips docs matching `ignore_inline_refs` config or `--ignore` flag patterns"
- **Why**: The term `ignored_paths` does not exist in the codebase. The actual mechanism uses `config.ignore_inline_refs` (config.py line 24) combined with `--ignore` CLI patterns (cli.py line 21), filtered via `_filter_parsed_cache()` (info.py lines 219-224).

### 9. Implementation Details: added new functions
- **What**: Added `extract_inline_refs()`, `find_undeclared_inline_refs()`, `_build_data()`, `_print_from_data()`, `_filter_parsed_cache()` to the function table
- **Why**: These functions exist in `info.py` and are part of the validation implementation. The table claims to list implementation details.

## Pre-existing Issues (not fixed)

### Behavior bullet: "Reports docs that fail to parse as validation errors"
- **Observation**: In `build_doc_index()` (docs.py lines 127-129), parse failures are caught with `except (OSError, UnicodeDecodeError, ValueError): continue` and silently skipped, not reported as validation errors.
- **Why not fixed**: This behavior predates the commits in scope. The changed files (`info.py`, `cli.py`, `config.py`, `filtering.py`) did not alter this parse-error handling.

## Sources Checked

- `src/doctrace/commands/info.py` - validation implementation (changed)
- `src/doctrace/cli.py` - --ignore flag definition (changed)
- `src/doctrace/core/config.py` - ignore_inline_refs config key (changed)
- `src/doctrace/core/filtering.py` - ignore pattern matching (new file)
- `src/doctrace/core/docs.py` - metadata extraction (unchanged)
- `docs/concepts.md` - required_doc (unchanged)
