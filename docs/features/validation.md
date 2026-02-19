---
title: Validation
description: Validates that all doc references point to existing files
required_docs:
  - docs/concepts.md: ValidateResult, RefError types
sources:
  - src/doctrace/commands/info.py: validation implementation
  - src/doctrace/core/docs.py: metadata extraction
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

Reports errors with file path and line number:

```
Warnings (2):
  docs/api.md:15: required doc not found: docs/missing.md
  docs/api.md:18: source not found: src/deleted.py
```

## Exit Codes

| Code | Meaning                    |
|------|----------------------------|
| 0    | all refs valid             |
| 1    | one or more refs invalid   |

## Output Format

Shows dependency phases followed by any validation warnings:

```
Independent (2):
  docs/concepts.md
  docs/utils.md

Phase 1 (1):
  docs/api.md

Warnings (1):
  docs/api.md:15: source not found: src/deleted.py
```

## Behavior

- Scans all `*.md` files recursively in target directory
- Skips docs matching ignored_paths patterns
- Reports docs that fail to parse as validation errors (continues scanning)
- All paths resolved relative to repo root

## Implementation Details

| Function             | Purpose                            |
|----------------------|------------------------------------|
| validate_refs()      | iterate docs, yield ValidateResults|
| _check_single_doc()  | validate one doc                   |
| _glob_matches()      | check if pattern has matches       |
| build_dependency_tree() | build doc dependency tree       |

