# Sync Report: docs/architecture.md

## Status: UPDATED

## Changes Applied

### 1. Fixed info.py description: "phases" -> "levels"
- **Line 42**: `info.py` comment changed from `"phases + validation"` to `"levels + validation"`
- **Reason**: The info command now uses "levels" terminology throughout (`_print_from_data` prints "Documentation Levels", "Level N:" labels). The "phases" term was renamed to "levels" in commit `511478d` (refactor(info): align output format with shell script).

### 2. Added filtering.py to core/ module listing
- **Line 49**: Added `filtering.py ← ignore pattern matching` to the core/ tree
- **Reason**: `src/doctrace/core/filtering.py` is a new file added in commit `706a305` (refactor: extract fnmatch filter to core/filtering.py). It is imported by both `info.py` and `affected.py`.

### 3. Removed depth_limit from propagation algorithm
- **Line 94**: Removed `depth_limit` from `_propagate()` annotation in affected data flow diagram
- **Lines 110-130**: Removed `depth_limit` from pseudocode Input, removed `depth = 0` initialization, removed `if depth_limit reached: break` check, removed `depth += 1` increment
- **Reason**: The actual `_propagate()` function in `affected.py` has no `depth_limit` parameter. It was removed in commit `6909a50` (predates the current commit range but is a factual error in the doc).

## Not Changed (Noted for Review)

### Entry Point diagram missing index and completion commands
- The Entry Point box diagram (lines 20-34) only shows info, affected, preview, init. The actual cli.py also registers `index` and `completion` commands. This predates recent changes and was not modified.

### Module Structure missing index.py, completion.py, cmd_registry.py
- The module tree (lines 38-52) omits `commands/index.py`, `commands/completion.py`, and `cmd_registry.py`. These files exist but predate the recent changes. Not modified.

### Propagation pseudocode circular ref detection differs from implementation
- The pseudocode shows circular refs detected inline during BFS traversal. The actual code detects them in a separate `_find_circular_refs()` post-processing step after BFS completes. This is a simplification difference that predates recent changes. Not modified per conservative editing rules.

### Data Flow - Info Command diagram is incomplete
- The info command now also performs undeclared inline ref validation and level computation, which are not shown in the data flow diagram. These were added in recent commits (`2cac932`, `511478d`). Not expanded per "never expand" rule, but the core validation flow shown is still accurate.

## Sources Reviewed
- src/doctrace/cli.py
- src/doctrace/cmd_registry.py
- src/doctrace/commands/affected.py
- src/doctrace/commands/info.py
- src/doctrace/commands/preview/graph.py
- src/doctrace/core/config.py
- src/doctrace/core/filtering.py
- src/doctrace/core/constants.py
