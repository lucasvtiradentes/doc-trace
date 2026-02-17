# Add Doc Metadata

Guide to adding metadata sections to documentation files.

## Metadata Format

Add a `---` separator followed by `related docs:` and/or `related sources:` sections at the end of your doc:

```markdown
# Your Doc Title

Content here...

---

related docs:
- docs/other-doc.md - description of relationship

related sources:
- src/path/to/file.py - description
- src/path/to/dir/ - description
```

## Section Format

### related docs:

References to other documentation files:

```
related docs:
- docs/concepts.md - defines types used here
- docs/api.md - API documentation
```

### related sources:

References to source code files or directories:

```
related sources:
- src/module.py - main implementation
- src/utils/ - utility functions
- tests/*.py - test files (glob pattern)
```

## Path Rules

All paths are relative to repository root:

```
Good:
- src/module.py            ← from repo root
- docs/api/endpoints.md    ← from repo root

Bad:
- ./src/module.py          ← don't use ./
- ../src/module.py         ← don't use ../
- /absolute/path.py        ← don't use absolute
```

## Line Item Format

Each item follows the pattern:

```
- path - description
```

| Component   | Required | Notes                           |
|-------------|----------|---------------------------------|
| `-`         | yes      | list marker                     |
| path        | yes      | relative path from repo root    |
| `-`         | yes      | separator                       |
| description | yes      | human-readable description      |

## Directory References

Trailing slash indicates directory (matches all files within):

```
related sources:
- src/booking/ - booking module
```

This doc is flagged if any file in `src/booking/` changes.

## Glob Patterns

Wildcards supported for source paths:

```
related sources:
- src/*.py - all Python files in src/
- tests/**/*.py - all test files recursively
```

## Example Doc

```markdown
# API Documentation

This doc covers the API endpoints.

## Endpoints

...content...

---

related docs:
- docs/concepts.md - type definitions
- docs/authentication.md - auth flow

related sources:
- src/api/ - API implementation
- src/models.py - data models
```

## Validation

After adding metadata, validate:

```bash
docsync check docs/
```

Errors show file path and line number:

```
docs/api.md:25: related doc not found: docs/missing.md
```

---

related docs:
- docs/concepts.md             - RefEntry, ParsedDoc types
- docs/guides/validate-docs.md - validation guide

related sources:
- src/docsync/core/parser.py - metadata parsing logic
