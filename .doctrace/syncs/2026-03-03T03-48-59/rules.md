# Sync Report: docs/rules.md

## Status: UPDATED

## Changes Made

### 1. Added missing commands to Single-Responsibility Commands list (line 17-22)
- **What**: Added `index` and `completion` commands to the list
- **Why**: `src/doctrace/commands/index.py` and `src/doctrace/commands/completion.py` were added to the codebase. The command list was factually incomplete, listing only 4 of 6 commands.
- **Source**: `src/doctrace/cli.py` (lines 38-43), `src/doctrace/cmd_registry.py` (lines 37-49)

### 2. Fixed command name in Lazy Error Recovery section (line 40)
- **What**: Changed `validate` to `info`
- **Why**: There is no `validate` command. The `info` command (`src/doctrace/commands/info.py`) is the one that performs validation via `validate_refs()`.
- **Source**: `src/doctrace/cli.py` (line 51), `src/doctrace/commands/info.py`

### 3. Fixed Lowercase CLI command list (line 57)
- **What**: Replaced `validate`, `affected`, `preview`, `lock`, `init` with `info`, `affected`, `preview`, `init`, `index`, `completion`
- **Why**: `validate` and `lock` do not exist as commands. The actual commands are `info`, `affected`, `preview`, `init`, `index`, `completion`.
- **Source**: `src/doctrace/cmd_registry.py` (COMMANDS dict), `src/doctrace/cli.py`

### 4. Removed reference to nonexistent `affected_depth_limit` (line 79)
- **What**: Removed "Use `affected_depth_limit`." from the Exhaustive Dependency Crawling anti-pattern
- **Why**: No `depth_limit` or `affected_depth_limit` parameter exists anywhere in the codebase. The `_propagate()` function in `affected.py` does not implement a depth limit.
- **Source**: `src/doctrace/commands/affected.py` (`_propagate` function, lines 103-122)

## Notes

- The "Future Annotations" section states "All command/core modules use `from __future__ import annotations`". `commands/init.py` does not include this import. This is a minor inaccuracy but was not changed since `init.py` is a trivial 4-line module that does not use any type annotations requiring the import.
- Frontmatter metadata was not changed; sources and related_docs references remain valid.

## Sources Reviewed
- src/doctrace/commands/affected.py
- src/doctrace/commands/completion.py
- src/doctrace/commands/index.py
- src/doctrace/commands/info.py
- src/doctrace/commands/init.py
- src/doctrace/commands/preview/server.py
- src/doctrace/core/config.py
- src/doctrace/core/docs.py
- src/doctrace/core/filtering.py
- src/doctrace/core/git.py
- src/doctrace/core/constants.py
- src/doctrace/cli.py
- src/doctrace/cmd_registry.py
- docs/architecture.md
- docs/concepts.md
