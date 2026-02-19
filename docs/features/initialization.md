---
title: Initialization
description: Creates the doctrace.json configuration file
related_docs:
  - docs/concepts.md: Config type
  - docs/guides/setup-project.md: project setup guide
sources:
  - src/doctrace/commands/init.py: init command
  - src/doctrace/core/config.py: init_config function
  - src/doctrace/core/constants.py: default config values
---

# Initialization (init command)

Creates the doctrace.json configuration file at repo root.

## Usage

```bash
doctrace init
```

## What It Creates

```
doctrace.json     ← configuration file at repo root
```

## Default doctrace.json

```json
{}
```

An empty object uses all defaults. You can customize metadata keys:

```json
{
  "metadata": {
    "required_docs_key": "required_docs",
    "related_docs_key": "related_docs",
    "sources_key": "sources"
  }
}
```

| Field                     | Default          | Description                        |
|---------------------------|------------------|------------------------------------|
| metadata.required_docs_key| "required_docs"  | frontmatter key for required docs  |
| metadata.related_docs_key | "related_docs"   | frontmatter key for related docs   |
| metadata.sources_key      | "sources"        | frontmatter key for source refs    |

## base

When you run `doctrace base update`, the file also stores the base commit:

```json
{
  "base": {
    "commit_hash": "abc123...",
    "commit_message": "feat: add feature",
    "commit_date": "2026-02-17T10:30:00+00:00",
    "analyzed_at": "2026-02-17T20:55:32+00:00"
  }
}
```

## Output

```
Created doctrace.json
```

## Implementation

Uses `init_config()` from config module:
1. Write empty doctrace.json at repo root
