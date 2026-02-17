# Affected (affected command)

Maps code changes to affected documentation.

## Usage

```bash
docsync affected docs/ --last 1
docsync affected docs/ --since-lock
docsync affected docs/ --base-branch main
docsync affected docs/ --since v0.1.0
docsync affected docs/ --last 5 --verbose
docsync affected docs/ --last 1 --json
```

## Output Formats

### Default

Shows direct hits, indirect hits (with propagation chain), and phases:

```
Direct hits (2):
  docs/api.md
  docs/booking.md

Indirect hits (1):
  docs/overview.md <- docs/api.md

Phases (2):
  1. docs/api.md, docs/booking.md
  2. docs/overview.md
```

### --verbose

Adds git context before the default output: changed files with status and line stats, commits, tags, merged branches, and source-to-doc matches.

### --json

Outputs the full result as JSON instead of text.

## How It Works

### Step 1: Get Changed Files

Resolves a comparison base from one required scope flag:
- `--last <N>` -> `HEAD~N`
- `--since-lock` -> `.docsync/lock.json:last_analyzed_commit`
- `--base-branch <branch>` -> `git merge-base HEAD <branch>`
- `--since <ref>` -> uses the ref directly (commit, tag, or branch)

Then runs `git diff --name-only <base>` to get changed source files.

### Step 2: Build Indexes

Scans all docs and builds two indexes:
- `source_to_docs` - which docs reference each source path
- `doc_to_docs`    - which docs reference each doc

### Step 3: Find Direct Hits

Matches changed files against source_to_docs:
- Exact path match: `src/module.py` matches `src/module.py`
- Directory match:  `src/booking/handler.py` matches `src/booking/` (trailing slash required)

### Step 4: Propagate

BFS traversal from direct hits through doc_to_docs:
- Level 0: direct hits
- Level 1: docs that reference level 0 docs
- Level N: docs that reference level N-1 docs

## Configuration

### affected_depth_limit

Limit how deep propagation goes.

```json
{
  "affected_depth_limit": 2
}
```

| Value | Behavior                      |
|-------|-------------------------------|
| null  | unlimited depth               |
| 0     | direct hits only              |
| N     | up to N levels of propagation |

## Circular Reference Detection

Detects revisits during propagation traversal.

- Reported as warnings
- Does not block processing
- Recorded as `(source_doc, revisited_doc)` tuples

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
                          _propagate()
                           (BFS)
                                │
                                v
                       AffectedResult
```

---

related docs:
- docs/concepts.md - AffectedResult type

related sources:
- src/docsync/commands/affected.py - affected implementation
- src/docsync/core/git.py - git helpers used by affected (FileChange, commits, tags)
- src/docsync/cli.py - CLI flag definitions for affected command
