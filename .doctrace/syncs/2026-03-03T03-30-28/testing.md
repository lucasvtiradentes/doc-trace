# Sync Report: docs/testing.md

## Sources Checked

- tests/affected/ (flagged: tests/affected/pure_logic/test_pure_logic.py)
- tests/parser/
- tests/preview/ (flagged: tests/preview/test_graph.py)
- tests/validate/ (new: tests/validate/inline_refs/)
- tests/config/
- tests/cli/ (flagged: tests/cli/test_affected_flags.py)
- tests/core/

## Related Docs Checked

- docs/repo/tooling.md
- docs/repo/cicd.md

## Changes Made

### 1. Added "inline refs" to tests/validate/ coverage description

- **Line 39**: Added `, inline refs` to the validate test coverage column
- **Reason**: New `tests/validate/inline_refs/` directory was added (commit 2cac932) with four test subdirectories: `valid/`, `missing/`, `code_block/`, `ignored/`. The previous description "valid refs, missing docs, missing sources" was factually incomplete.

## No Change Needed

### tests/affected/ coverage description

The description says "index building, direct hits, propagation, scope resolution". The `pure_logic` tests now also include `_filter_docs` tests (for `--ignore` patterns), which could be considered an addition. However, filtering is part of the broader affected-docs logic and the existing description is not factually wrong -- it just does not enumerate every sub-feature. Kept as-is per conservative editing rules.

### tests/preview/ coverage description

The `test_graph.py` file had an internal rename from "Independent" to "Level 0" (commit c68c970), but this is an internal assertion change. The tests still cover "search, graph building". No doc change needed.

### tests/cli/ coverage description

The `test_affected_flags.py` added new tests for `--since` and `--ignore` flags. The description "CLI argument parsing and command dispatch" is still accurate as a category-level description. No doc change needed.

### Frontmatter sources

All source directory references (`tests/affected/`, `tests/validate/`, etc.) use directory paths that correctly cover both existing and new test files. No frontmatter changes needed.

## Summary

| Metric | Count |
|--------|-------|
| Lines changed | 1 |
| Factual fixes | 1 |
| Rephrases | 0 |
| Additions | 0 |
