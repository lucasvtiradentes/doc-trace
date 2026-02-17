## Confidence
high

## Files read
- src/docsync/core/parser.py - RefEntry, ParsedDoc definitions; both match doc accurately
- src/docsync/commands/affected.py - AffectedResult now has 6 fields (was 4 in doc); major refactoring added matches and indirect_chains fields
- src/docsync/commands/validate.py - ValidateResult, RefError definitions; both match doc accurately
- src/docsync/core/config.py - Config, MetadataConfig definitions; both match doc accurately
- src/docsync/core/lock.py - Lock definition; matches doc accurately
- src/docsync/core/git.py - new module with FileChange, CommitInfo types used by affected.py

## Metadata updates
- Added source: src/docsync/core/git.py (defines FileChange and CommitInfo types used in affected command output; created in commit aa94b0a)

## Changes made
- Added two missing fields to AffectedResult table: matches (dict[str, list[Path]]) and indirect_chains (dict[Path, Path])
- Added src/docsync/core/git.py to related sources metadata

## Why it was wrong
- AffectedResult was refactored in commit b7fe847 ("feat: add git info to verbose, refactor to data-first architecture") to include matches and indirect_chains fields. The doc only listed the original 4 fields, missing these 2 new fields that are actively used in _build_output_data and _build_git_data for verbose/json output.
- src/docsync/core/git.py was created in commit aa94b0a ("refactor: consolidate git operations into core/git.py") and defines types (FileChange, CommitInfo) that are core data structures used by affected.py, making it a relevant source for this concepts doc.
