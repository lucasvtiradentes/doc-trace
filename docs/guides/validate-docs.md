# Validate Docs

Guide to validating documentation references.

## Basic Validation

```bash
docsync check docs/
```

Scans all `*.md` files in `docs/` recursively and validates:
- `related docs:` paths exist
- `related sources:` paths exist (or glob matches)

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

## Ignoring Paths

Create `.docsync/config.json` to skip certain docs:

```json
{
  "ignored_paths": [
    "docs/drafts/*.md",
    "docs/archive/*",
    "docs/wip.md"
  ]
}
```

Patterns use fnmatch syntax:
- `*` matches any characters except `/`
- `**` matches any characters including `/`
- `?` matches single character

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
- run: docsync check docs/
```

Fails build if any refs are invalid.

## Parse Errors

Docs that fail to parse are skipped with error message:

```
docs/broken.md:0: failed to parse doc: ...
```

This does not block validation of other docs.

## Workflow

1. Add/edit metadata in docs
2. Run `docsync check docs/`
3. Fix any reported errors
4. Commit changes

---

related docs:
- docs/features/validation.md     - check command details
- docs/guides/add-doc-metadata.md - metadata format

related sources:
- src/docsync/commands/check.py - validation implementation
