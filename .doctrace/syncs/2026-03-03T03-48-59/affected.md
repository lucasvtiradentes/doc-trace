# Sync Report: docs/features/affected.md

## Sources Reviewed

- src/doctrace/commands/affected.py
- src/doctrace/core/git.py
- src/doctrace/cli.py
- src/doctrace/core/filtering.py (new dependency)

## Required Docs Reviewed

- docs/concepts.md (Phase 1, updated: added ParsedDoc fields, RefError field)

## Related Docs Reviewed

- docs/overview.md (Phase 1, updated: version fix)

## Changes Applied

### 1. Added missing source to frontmatter

**Location**: frontmatter `sources` section

**What changed**: Added `src/doctrace/core/filtering.py` to the sources list.

**Why**: The affected command now imports and uses `matches_ignore_pattern` from `src/doctrace/core/filtering.py` (extracted in commit `706a305`). This is a real source dependency -- if `filtering.py` changes, this doc should be reviewed. Without it in the sources list, doc-trace would not flag this doc when filtering logic changes.

## No Change Needed

### Usage examples (lines 17-21)

The four usage examples (`--last`, `--base-branch`, `--since`, `--json`) are all correct. The removed `--since-base` flag was never shown in the doc's examples, so no update needed.

### Output format description (lines 27-51)

The doc describes the default output as showing git context (changed files, commits, tags, merged branches, source-to-doc matches), direct hits, indirect hits, and phases. This was previously only shown with `--verbose`, but commit `89d4495` made verbose the default. The doc already described this as "Default" output, so it is now factually correct for the current code.

### Scope flags (lines 61-64)

The doc lists three scope flags: `--last`, `--base-branch`, `--since`. This matches the current `resolve_commit_ref` function which accepts exactly these three (the removed `--since-base` was never documented here).

### Step descriptions (lines 59-85)

- Step 1 (Get Changed Files): Correctly describes `resolve_commit_ref` logic and `git diff --name-only`.
- Step 2 (Build Indexes): `source_to_docs` and `doc_to_docs` correctly describe what `build_doc_index` produces. The `doc_to_docs` name matches the parameter name used in `_propagate`.
- Step 3 (Find Direct Hits): Exact path match and directory match (trailing slash) logic matches `_find_direct_hits` code.
- Step 4 (Propagate): BFS traversal description matches `_propagate` implementation.

### Circular Reference Detection (lines 87-93)

The description says "Detects revisits during propagation traversal." In reality, circular detection happens post-traversal via `_find_circular_refs`, not during BFS traversal. However, this was already the case before these changes -- the `_find_circular_refs` function is unchanged. Not fixing pre-existing imprecision per conservative rules.

### Implementation diagram (lines 97-114)

The diagram accurately reflects the code flow: git diff -> changed_files -> build_doc_index() -> _find_direct_hits() -> _propagate() -> AffectedResult.

## Not Documented (Noted Only)

### --ignore flag

The `--ignore` flag was added to the affected command CLI (visible in `cli.py` line 30). It allows filtering out docs matching fnmatch patterns. The affected command's `run` function accepts `ignore_patterns` and uses `_filter_docs` with `matches_ignore_pattern` from `core/filtering.py`. This is not documented in the current doc. Per conservative editing rules, not adding new feature documentation that was never present.
