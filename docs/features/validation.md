---
title: Validation
description: Validates that all doc references point to existing files
required_docs:
  - docs/concepts.md: ValidateResult, RefError types
sources:
  - src/doctrace/commands/info.py:    validation implementation
  - src/doctrace/core/docs.py:        metadata extraction
  - src/doctrace/cli.py:              --ignore flag definition
  - src/doctrace/core/config.py:      ignore_inline_refs config key
  - src/doctrace/core/filtering.py:   ignore pattern matching
---

Validates that all doc references point to existing files and shows dependency levels.

## Usage

```bash
doctrace info docs/
doctrace info docs/ --ignore "docs/drafts/*"
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

### Undeclared Inline Refs

Detects `docs/` paths referenced in the doc body that are not declared in `required_docs:` or `related_docs:`. Ignores refs inside code blocks and inline code spans.

## Error Output

Reports errors grouped by section:

```
## Missing Referenced Docs
----------------------------------------
ERROR: Referenced docs not found!
  docs/api.md -> docs/missing.md (required)
  docs/api.md -> src/deleted.py (source)
```

## Exit Codes

| Code | Meaning                                                      |
|------|--------------------------------------------------------------|
| 0    | all refs valid                                               |
| 1    | circular deps, missing refs, or undeclared inline refs found |

## Output Format

Shows sections for circular dependencies, missing refs, dependency levels, inline ref checks, and a summary:

```
## Documentation Levels (by required_docs depth)
----------------------------------------

Level 0:
  docs/concepts.md  (req: 0, rel: 0)
  docs/utils.md     (req: 0, rel: 1)

Level 1:
  docs/api.md       (req: 1, rel: 0)

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
- Skips docs matching `ignore_inline_refs` config or `--ignore` flag patterns
- Reports docs that fail to parse as validation errors (continues scanning)
- All paths resolved relative to repo root

## Implementation Details

| Function                      | Purpose                                    |
|-------------------------------|--------------------------------------------|
| validate_refs()               | iterate docs, yield ValidateResults        |
| _check_single_doc()           | validate one doc                           |
| _glob_matches()               | check if pattern has matches               |
| extract_inline_refs()         | find doc refs in markdown body             |
| find_undeclared_inline_refs() | detect inline refs not in frontmatter      |
| _build_data()                 | assemble output data dict                  |
| _print_from_data()            | print formatted output with section headers|
| _filter_parsed_cache()        | filter docs by ignore patterns             |
| build_dependency_tree()       | build doc dependency tree                  |

