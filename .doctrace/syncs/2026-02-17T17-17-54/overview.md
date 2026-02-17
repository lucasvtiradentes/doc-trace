## Confidence
high

## Files read
- src/docsync/cli.py - verified commands list, entry point, CLI structure; confirmed no tree command exists
- src/docsync/core/git.py - new file with git helper functions (FileChange, get_changed_files_detailed, get_commits_in_range, etc.); used by affected command for verbose/git info
- src/docsync/commands/preview/__init__.py - confirmed preview command exists and delegates to server.py
- src/docsync/commands/affected.py - confirmed verbose and json flags, git data integration
- src/docsync/__init__.py - confirmed public API exports
- pyproject.toml - confirmed version is 0.1.1, python >=3.9, entry point docsync.cli:main, hatch build

## Changes made
- Updated version from 0.1.0 to 0.1.1 in Package Info table

## Why it was wrong
- The version in docs/overview.md said 0.1.0 but pyproject.toml has version 0.1.1. The git context shows commits since v0.1.1 tag, confirming the version bump already happened.
