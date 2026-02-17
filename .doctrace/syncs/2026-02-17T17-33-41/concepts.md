## Confidence
high

## Files read
- src/docsync/core/parser.py - RefEntry, ParsedDoc definitions; unchanged, doc is accurate
- src/docsync/commands/affected.py - AffectedResult now has 6 fields (was 4); added matches and indirect_chains
- src/docsync/commands/validate.py - ValidateResult, RefError definitions; unchanged, doc is accurate
- src/docsync/core/config.py - Config, MetadataConfig definitions; unchanged, doc is accurate
- src/docsync/core/lock.py - Lock definition; fields unchanged, only import refactored (get_current_commit moved to core/git.py)
- src/docsync/core/git.py - new module with FileChange, CommitInfo types and git helpers; not documented in concepts but not a doc dependency

## Metadata updates
- No metadata changes

## Changes made
- Added two missing fields to AffectedResult table: matches (dict[str, list[Path]]) and indirect_chains (dict[Path, Path])

## Why it was wrong
- AffectedResult in src/docsync/commands/affected.py was expanded in commit b7fe847 (data-first architecture refactor) to include matches and indirect_chains fields. The doc only listed the original 4 fields, missing the 2 new ones that are part of the public NamedTuple returned by find_affected_docs.
