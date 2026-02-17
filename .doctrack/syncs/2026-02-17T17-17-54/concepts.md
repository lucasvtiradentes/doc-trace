## Confidence
high

## Files read
- src/docsync/core/parser.py - RefEntry and ParsedDoc NamedTuples; unchanged, doc was accurate
- src/docsync/commands/affected.py - AffectedResult now has 6 fields (added matches, indirect_chains); major refactor to data-first architecture
- src/docsync/commands/validate.py - ValidateResult and RefError; unchanged, doc was accurate
- src/docsync/core/config.py - Config and MetadataConfig; unchanged, doc was accurate
- src/docsync/core/lock.py - Lock class; fields unchanged, now imports get_current_commit from core/git
- src/docsync/core/git.py - new file; defines FileChange, CommitInfo, and git helper functions used by affected.py

## Changes made
- Added 2 missing fields to AffectedResult table: matches (dict[str, list[Path]]) and indirect_chains (dict[Path, Path])
- Added src/docsync/core/git.py to related sources metadata (new file defining FileChange and CommitInfo types)

## Why it was wrong
- AffectedResult in src/docsync/commands/affected.py was refactored (commit "feat: add git info to verbose, refactor to data-first architecture") to include matches and indirect_chains fields. The doc only listed the original 4 fields, missing these 2 new ones that are integral to the data-first output architecture.
- src/docsync/core/git.py was added (commit "refactor: consolidate git operations into core/git.py") as a new module defining FileChange and CommitInfo types used by affected.py. The doc's related sources did not reference this file.
