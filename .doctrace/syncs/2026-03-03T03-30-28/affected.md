# Sync Report: docs/features/affected.md

## Sources Checked

- src/doctrace/commands/affected.py
- src/doctrace/core/git.py
- src/doctrace/cli.py
- src/doctrace/cmd_registry.py
- src/doctrace/core/filtering.py
- src/doctrace/core/config.py
- docs/concepts.md (required_doc)

## Changes Applied

### 1. Added missing source to frontmatter

`src/doctrace/core/filtering.py` is now imported and used by `affected.py` (the `_filter_docs` function calls `matches_ignore_pattern` from `filtering.py`). Added it to the `sources:` frontmatter list.

**Diff:**
```
 sources:
   - src/doctrace/commands/affected.py: affected implementation
   - src/doctrace/core/git.py:          git helpers used by affected (FileChange, commits, tags)
   - src/doctrace/cli.py:               CLI flag definitions for affected command
+  - src/doctrace/core/filtering.py:    ignore pattern matching used by _filter_docs
```

## No Change Needed

- **--since-base**: Not mentioned anywhere in the doc. No fix needed.
- **--verbose / -V**: Not mentioned anywhere in the doc. No fix needed.
- **doctrace.json / base command**: Not referenced in the doc. No fix needed.
- **Usage examples (--last, --base-branch, --since)**: All three scope flags still exist in source code. Verified in `cli.py` (lines 26-28) and `affected.py` `resolve_commit_ref` (lines 33-53). No fix needed.
- **Output format section**: Describes the verbose/detailed output which is now the default (and only) format. The doc labels it "Default" which is accurate. No fix needed.
- **How It Works steps**: All four steps (Get Changed Files, Build Indexes, Find Direct Hits, Propagate) remain accurate per source code. No fix needed.
- **Circular Reference Detection**: Description is accurate. `_find_circular_refs` is still called from `_propagate`. No fix needed.
- **Implementation diagram**: Flow still matches: git diff -> changed_files -> build_doc_index() -> _find_direct_hits() -> _propagate() -> AffectedResult. No fix needed.
- **--json flag**: Still exists in cli.py (line 29) and affected.py `run()`. No fix needed.

## Notes

- The `--ignore` flag was added to the affected command (cli.py line 30, cmd_registry.py line 23, affected.py `run()` line 314). The doc does not document this flag. However, the doc never had a comprehensive flags/options section -- it only documents `--json` in a subsection and the three scope flags in "How It Works." Adding `--ignore` documentation would be expanding the doc rather than fixing a factual error. Flagging for manual review.
- The `run()` function now includes a `_filter_docs` step that filters results through ignore patterns before output. The Implementation diagram does not show this step. This is a minor omission in an overview diagram rather than a factual error. Flagging for manual review.
- `cmd_registry.py` confirms affected flags are: `--last`, `--base-branch`, `--since`, `--json`, `--ignore`. The doc covers all except `--ignore`.
