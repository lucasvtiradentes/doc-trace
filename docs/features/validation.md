---
title: Validation
description: Validates that all doc references point to existing files
required_docs:
  - docs/concepts.md: ValidateResult, RefError types
sources:
  - src/doctrace/commands/info.py: validation implementation
  - src/doctrace/core/docs.py:     metadata extraction
---

Validates that all doc references point to existing files and shows dependency phases.

## Usage

```bash
doctrace info docs/
```

## What It Checks

### Required Docs

Verifies each path in `required_docs:` section exists as a file.

```
required_docs:
  - docs/other.md: description    ← must exist
```

### Related Docs

Verifies each path in `related_docs:` section exists as a file.

```
related_docs:
  - docs/other.md: description    ← must exist
```

### Sources

Verifies each path in `sources:` section exists. Supports:
- Exact file paths
- Directory paths
- Glob patterns (*, ?)

```
sources:
  - src/module.py: exact file     ← must exist
  - src/utils/: directory         ← must exist
  - src/*.py: glob pattern        ← must match at least one file
```

## Error Output

Reports errors under dedicated section headers:

```
## Missing Referenced Docs
----------------------------------------
ERROR: Referenced docs not found!
  docs/api.md -> docs/missing.md (required)
  docs/api.md -> src/deleted.py (source)
```

## Exit Codes

| Code | Meaning                                                               |
|------|-----------------------------------------------------------------------|
| 0    | all refs valid                                                        |
| 1    | errors found (missing refs, circular deps, or undeclared inline refs) |

## Output Format

Shows a structured report with sections for circular deps, missing refs, levels, inline refs, and summary:

```
============================================================
DOCUMENTATION DEPENDENCY ANALYSIS
============================================================

## Documentation Levels (by required_docs depth)
----------------------------------------

Level 0:
  docs/concepts.md  (req: 0, rel: 1)
  docs/utils.md     (req: 0, rel: 0)

Level 1:
  docs/api.md  (req: 1, rel: 0)

## Summary
----------------------------------------
Total docs: 3
Levels: 2 (0 to 1)
Circular deps (required): 0
Missing referenced docs: 0
Missing inline refs: 0
```

## Behavior

- Scans all `*.md` files recursively in target directory
- Skips docs matching ignore_inline_refs config patterns and --ignore CLI patterns
- Silently skips docs that fail to parse (continues scanning)
- All paths resolved relative to repo root

## Implementation Details

| Function                | Purpose                             |
|-------------------------|-------------------------------------|
| validate_refs()         | iterate docs, yield ValidateResults |
| _check_single_doc()     | validate one doc                    |
| _glob_matches()         | check if pattern has matches        |
| build_dependency_tree() | build doc dependency tree           |

