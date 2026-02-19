---
title: Initialization
description: Creates the .doctrace/ configuration directory
related_docs:
  - docs/concepts.md: Config type
  - docs/guides/setup-project.md: project setup guide
sources:
  - src/doctrace/commands/init.py: init command
  - src/doctrace/core/config.py: init_doctrace function
  - src/doctrace/core/constants.py: default config values
---

# Initialization (init command)

Creates the .doctrace/ configuration directory.

## Usage

```bash
doctrace init
```

## What It Creates

```
.doctrace/
└── config.json     ← default configuration
```

## Default config.json

```json
{
  "ignored_paths": [],
  "affected_depth_limit": null,
  "metadata": {
    "required_docs_key": "required_docs",
    "related_docs_key": "related_docs",
    "sources_key": "sources"
  }
}
```

| Field                     | Default          | Description                        |
|---------------------------|------------------|------------------------------------|
| ignored_paths             | []               | patterns to skip in validation     |
| affected_depth_limit      | null             | max propagation depth (unlimited)  |
| metadata.required_docs_key| "required_docs"  | frontmatter key for required docs  |
| metadata.related_docs_key | "related_docs"   | frontmatter key for related docs   |
| metadata.sources_key      | "sources"        | frontmatter key for source refs    |

## Idempotent

Running `init` multiple times is safe:
- Existing config.json is overwritten with defaults

## Output

```
Created .doctrace/
```

## Implementation

Uses `init_doctrace()` from config module:
1. Create .doctrace/ directory
2. Write config.json with defaults
