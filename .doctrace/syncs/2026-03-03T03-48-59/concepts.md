# Sync Report: docs/concepts.md

## Status: UPDATED

## Changes Made

### 1. ParsedDoc: added missing `title` and `description` fields
- **Location**: ParsedDoc table (line 28-34)
- **Issue**: `ParsedDoc` in source code (`src/doctrace/core/docs.py` lines 22-27) has five fields: `required_docs`, `related_docs`, `sources`, `title`, and `description`. The doc only listed the first three.
- **Cause**: Commit `0ebacd1` (feat: add index command to generate index.md from frontmatter) added `title: str` and `description: str` fields to ParsedDoc.
- **Fix**: Added `title` and `description` rows to the ParsedDoc table.

### 2. RefError: added missing `ref_type` field
- **Location**: RefError table (line 105-110)
- **Issue**: `RefError` in source code (`src/doctrace/commands/info.py` lines 16-20) has four fields: `doc_path`, `ref`, `message`, and `ref_type`. The doc only listed the first three.
- **Cause**: The info.py diff shows `ref_type: str` was added to the `RefError` dataclass, used to distinguish between "required", "related", and "source" ref types in validation errors.
- **Fix**: Added `ref_type` row to the RefError table.

## Verified Accurate (no changes needed)

- **RefEntry**: 3 fields match source (`path`, `description`, `line_number`)
- **DocIndex**: 4 fields match source (`parsed_cache`, `source_to_docs`, `forward_deps`, `reverse_deps`)
- **DependencyTree**: 4 fields match source (`levels`, `circular`, `doc_deps`, `index`)
- **AffectedResult**: 7 fields match source (all correct)
- **Config**: 2 fields match source (`metadata`, `ignore_inline_refs`)
- **MetadataConfig**: 3 fields match source with correct defaults
- **ValidateResult**: 3 fields match source (`doc_path`, `errors`, `ok` property)
- **Terminology section**: All definitions (Direct Hit, Indirect Hit, Circular Dependency, Metadata Section) are accurate
- **Frontmatter sources**: All 5 source paths exist and descriptions are accurate

## Sources Checked

- `src/doctrace/core/docs.py` - RefEntry, ParsedDoc, DocIndex, DependencyTree
- `src/doctrace/commands/affected.py` - AffectedResult
- `src/doctrace/commands/info.py` - ValidateResult, RefError
- `src/doctrace/core/config.py` - Config, MetadataConfig
- `src/doctrace/core/git.py` - FileChange, CommitInfo, CurrentCommitInfo
