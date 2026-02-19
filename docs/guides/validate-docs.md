---
title: Validate Docs
description: Guide to validating documentation references
required_docs:
  - docs/features/validation.md: validate command details
sources:
  - src/doctrace/commands/info.py: info command implementation
---

Guide to validating documentation references.

## Basic Validation

```bash
doctrace info docs/
```

Scans all `*.md` files in `docs/` recursively and validates:
- `required_docs:` paths exist
- `related_docs:` paths exist
- `sources:` paths exist (or glob pattern matches)

## Success Output

```
All refs valid
```

Exit code: 0

## Error Output

```
docs/api.md:15: related doc not found: docs/missing.md
docs/api.md:18: related source not found: src/deleted.py
```

Exit code: 1

## Configuration

Create `doctrace.json` at repo root to customize metadata keys:

```json
{
  "metadata": {
    "required_docs_key": "required_docs",
    "related_docs_key": "related_docs",
    "sources_key": "sources"
  }
}
```

## Common Issues

### Missing Related Doc

```
docs/api.md:12: related doc not found: docs/typo.md
```

Fix: Correct the path or create the referenced doc.

### Missing Related Source

```
docs/api.md:15: related source not found: src/old-module.py
```

Fix: Update path to current location or remove if deleted.

### Glob Pattern No Matches

```
docs/api.md:18: related source not found: src/legacy/*.py
```

Fix: Check glob pattern matches at least one file.

## Integration with CI

Add to your workflow:

```yaml
- run: doctrace info docs/
```

Fails build if any refs are invalid.

## Parse Errors

Docs that fail to parse are reported as errors:

```
docs/broken.md:0: failed to parse doc: ...
```

Validation continues for other docs, but command exits with code `1` if any parse error is reported.

## Workflow

1. Add/edit metadata in docs
2. Run `doctrace info docs/`
3. Fix any reported errors
4. Commit changes

