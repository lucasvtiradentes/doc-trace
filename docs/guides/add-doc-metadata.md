---
title: Add Doc Metadata
description: Guide to adding metadata sections to documentation files
required_docs:
  - docs/concepts.md: RefEntry, ParsedDoc types
sources:
  - src/doctrace/core/parser.py: metadata parsing logic
---

# Add Doc Metadata

Guide to adding metadata sections to documentation files.

## Format

Add YAML frontmatter at the top of the doc:

```markdown
---
title: Your Doc Title
description: Brief description of the doc
required_docs:
  - docs/dependency.md: needed to understand this doc
related_docs:
  - docs/related.md: related but not required
sources:
  - src/module.py: main implementation
  - src/utils/: utility directory
---

# Your Doc Title

Content here...
```

## Section Meanings

### required_docs

Hard dependencies - docs that must be understood first. Used for:
- Propagation in affected analysis
- Building doc phases/levels
- Detecting circular dependencies (error)

```yaml
required_docs:
  - docs/concepts.md: defines types used here
  - docs/architecture.md: system design context
```

### related_docs

Soft references - related but not required. Used for:
- Informational cross-references
- Bidirectional reference detection

```yaml
related_docs:
  - docs/api.md: API documentation
  - docs/guides/setup.md: setup guide
```

### sources

Code references - files/directories this doc describes:

```yaml
sources:
  - src/module.py: main implementation
  - src/utils/: utility functions directory
  - tests/*.py: test files (glob pattern)
```

## Path Rules

All paths are relative to repository root:

```
Good:
- src/module.py            <- from repo root
- docs/api/endpoints.md    <- from repo root

Bad:
- ./src/module.py          <- don't use ./
- ../src/module.py         <- don't use ../
- /absolute/path.py        <- don't use absolute
```

## Item Format

Each item follows YAML format with colon separator:

```yaml
  - path: description
```

| Component   | Required | Notes                        |
|-------------|----------|------------------------------|
| `-`         | yes      | list marker                  |
| path        | yes      | relative path from repo root |
| `:`         | yes      | separator                    |
| description | optional | human-readable description   |

## Directory and Glob References

The parser stores paths exactly as written:

```yaml
sources:
  - src/booking/: booking module
  - src/*.py: all Python files in src/
  - tests/**/*.py: all test files recursively
```

## Example Doc

```markdown
---
title: API Documentation
description: API endpoints and handlers
required_docs:
  - docs/concepts.md: type definitions
related_docs:
  - docs/authentication.md: auth flow
sources:
  - src/api/: API implementation
  - src/models.py: data models
---

# API Documentation

This doc covers the API endpoints.

## Endpoints

...content...
```

## Validation

After adding metadata, validate:

```bash
doctrace validate docs/
```

Errors show file path and line number:

```
docs/api.md:5: required doc not found: docs/missing.md
docs/api.md:10: source not found: src/deleted.py
```
