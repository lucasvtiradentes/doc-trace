# Validation (validate command)

Validates that all doc references point to existing files.

## Usage

```bash
docsync validate docs/
```

## What It Checks

### Related Docs

Verifies each path in `related docs:` section exists as a file.

```
related docs:
- docs/other.md - description    ← must exist
```

### Related Sources

Verifies each path in `related sources:` section exists. Supports:
- Exact file paths
- Directory paths
- Glob patterns (*, ?)

```
related sources:
- src/module.py - exact file     ← must exist
- src/utils/    - directory      ← must exist
- src/*.py      - glob pattern   ← must match at least one file
```

## Error Output

Reports errors with file path and line number:

```
docs/api.md:15: related doc not found: docs/missing.md
docs/api.md:18: related source not found: src/deleted.py
```

## Exit Codes

| Code | Meaning                    |
|------|----------------------------|
| 0    | all refs valid             |
| 1    | one or more refs invalid   |

## Configuration

### ignored_paths

Skip validation for matching docs.

```json
{
  "ignored_paths": [
    "docs/drafts/*.md",
    "docs/archive/*"
  ]
}
```

Patterns use fnmatch syntax.

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
| _is_ignored()        | check against ignored_paths        |

---

related docs:
- docs/concepts.md             - ValidateResult, RefError types
- docs/guides/validate-docs.md - usage guide

related sources:
- src/docsync/commands/validate.py - validation implementation
- src/docsync/core/parser.py       - metadata extraction
