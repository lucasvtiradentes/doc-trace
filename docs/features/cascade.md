# Cascade (cascade command)

Maps code changes to affected documentation.

## Usage

```bash
docsync cascade HEAD~1
docsync cascade abc123 --docs path/to/docs
```

## How It Works

### Step 1: Get Changed Files

Runs `git diff --name-only <commit>` to get list of changed source files.

### Step 2: Build Indexes

Scans all docs and builds two indexes:
- `source_to_docs` - which docs reference each source path
- `doc_to_docs`    - which docs reference each doc

### Step 3: Find Direct Hits

Matches changed files against source_to_docs:
- Exact path match: `src/module.py` matches `src/module.py`
- Directory match:  `src/booking/handler.py` matches `src/booking/` (trailing slash required)

### Step 4: Cascade

BFS traversal from direct hits through doc_to_docs:
- Level 0: direct hits
- Level 1: docs that reference level 0 docs
- Level N: docs that reference level N-1 docs

## Output

```
Direct hits (2):
  docs/api.md
  docs/booking.md

Cascade hits (1):
  docs/overview.md

Warning: circular refs detected:
  docs/a.md <-> docs/b.md
```

## Configuration

### cascade_depth_limit

Limit how deep cascade propagates.

```json
{
  "cascade_depth_limit": 2
}
```

| Value | Behavior                    |
|-------|-----------------------------|
| null  | unlimited depth             |
| 0     | direct hits only            |
| N     | up to N levels of cascade   |

## Circular Reference Detection

Detects when doc A → doc B → doc A (directly or indirectly).

- Reported as warnings
- Does not block processing
- Circular docs still included in results

## Implementation

```
┌────────────────┐     ┌─────────────────┐
│ git diff       │────→│ changed_files   │
└────────────────┘     └────────┬────────┘
                                │
┌────────────────┐              v
│ docs/*.md      │────→ _build_indexes()
└────────────────┘              │
                                v
                       _find_direct_hits()
                                │
                                v
                          _cascade()
                           (BFS)
                                │
                                v
                       CascadeResult
```

---

related docs:
- docs/architecture.md               - detailed data flow diagrams
- docs/concepts.md                   - CascadeResult type
- docs/features/prompt-generation.md - uses cascade for incremental mode

related sources:
- src/docsync/commands/cascade.py - cascade implementation
