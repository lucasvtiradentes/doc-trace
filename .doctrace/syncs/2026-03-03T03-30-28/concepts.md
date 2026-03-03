# Sync Report: docs/concepts.md

## Status: UPDATED

## Changes Made

### 1. Added missing `ref_type` field to RefError table
- **Section**: RefError
- **Issue**: The `RefError` dataclass in `src/doctrace/commands/info.py` now has a `ref_type: str` field (added in commits `d7935cc` and `511478d`), but the doc table only listed `doc_path`, `ref`, and `message`.
- **Fix**: Added `| ref_type | str | type of reference |` row to the RefError table.
- **Confidence**: High. The field is clearly present in the source at line 20 of `info.py` and is used throughout the validation logic (e.g., `_check_single_doc` passes `"required"`, `"related"`, `"source"` as ref_type values).

## No Changes Needed

- **RefEntry**: All 3 fields match source (`path`, `description`, `line_number`).
- **DocIndex**: All 4 fields match source.
- **DependencyTree**: All 4 fields match source.
- **AffectedResult**: All 7 fields match source.
- **Config**: Both fields match source (`metadata`, `ignore_inline_refs`).
- **MetadataConfig**: All 3 fields match source with correct defaults.
- **ValidateResult**: All fields match source including `ok` property.
- **Terminology sections**: Direct Hit, Indirect Hit, Circular Dependency, Metadata Section descriptions remain accurate.
- **Frontmatter sources**: All 5 source files exist and are relevant. No sources need adding or removing.

## Notes

- **ParsedDoc** is missing `title: str` and `description: str` fields that exist in source. This predates the current changes (added in commit `0ebacd1 feat: add index command`), so it was not modified per conservative editing rules. The existing 3 fields are documented accurately.
- The deletion of `src/doctrace/commands/base.py` and removal of the `Base` class from `config.py` do not affect this doc since neither was documented here.
- The rename from "Independent" to "Level 0" in preview/graph.py does not affect this doc since the term does not appear in it.
- The new `src/doctrace/core/filtering.py` module is a utility, not a type definition, and does not warrant a frontmatter source entry in this concepts doc.

## Sources Reviewed
- `src/doctrace/core/docs.py` - RefEntry, ParsedDoc, DocIndex, DependencyTree
- `src/doctrace/commands/affected.py` - AffectedResult
- `src/doctrace/commands/info.py` - ValidateResult, RefError
- `src/doctrace/core/config.py` - Config, MetadataConfig
- `src/doctrace/core/git.py` - FileChange, CommitInfo, CurrentCommitInfo
- `src/doctrace/core/filtering.py` - matches_ignore_pattern utility
