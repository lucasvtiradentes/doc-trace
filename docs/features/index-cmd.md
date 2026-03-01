---
title: Index Command
description: Generates index.md table from frontmatter metadata
related_docs:
  - docs/concepts.md: DocMeta type
  - docs/features/validation.md: uses same frontmatter parsing
sources:
  - src/doctrace/commands/index.py: index command
  - src/doctrace/core/docs.py: frontmatter parsing
---

Generates an index table from all docs' frontmatter metadata.

## Usage

```bash
doctrace index docs/ -o docs/index.md
```

## What It Does

1. Scans all `.md` files in the directory
2. Extracts `title` and `description` from frontmatter
3. Counts `required_docs`, `related_docs`, and `sources` entries
4. Generates a markdown table sorted by filename

## Output Format

```markdown
## Doc Index

| File                       | Description                    |
|----------------------------|--------------------------------|
| docs/overview.md           | project summary                |
| docs/architecture.md       | system design details          |
```

## Frontmatter Fields Used

| Field       | Required | Description                    |
|-------------|----------|--------------------------------|
| title       | no       | doc title (defaults to filename)|
| description | no       | short description              |

## Options

| Option          | Required | Description        |
|-----------------|----------|--------------------|
| `path`          | yes      | docs directory     |
| `-o`, `--output`| yes      | output file path   |

## Implementation

Uses `get_docs_metadata()` to extract frontmatter, then generates markdown table.
