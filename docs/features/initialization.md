# Initialization (init command)

Creates the .doctrack/ configuration directory.

## Usage

```bash
doctrack init
```

## What It Creates

```
.doctrack/
├── config.json     ← default configuration
└── syncs/          ← AI sync report storage
```

## Default config.json

```json
{
  "ignored_paths": [],
  "affected_depth_limit": null,
  "metadata": {
    "style": "custom",
    "docs_key": "related docs",
    "sources_key": "related sources",
    "require_separator": true
  }
}
```

| Field                     | Default          | Description                        |
|---------------------------|------------------|------------------------------------|
| ignored_paths             | []               | patterns to skip in validation     |
| affected_depth_limit      | null             | max propagation depth (unlimited)  |
| metadata.style            | "custom"         | "custom" or "frontmatter"          |
| metadata.docs_key         | "related docs"   | header for doc refs section        |
| metadata.sources_key      | "related sources"| header for source refs section     |
| metadata.require_separator| true             | require --- before metadata        |

## syncs/ Directory

Storage for AI-generated sync reports.

`init` updates the repository root `.gitignore` to include:

```
.doctrack/syncs/
```

If `.gitignore` already exists, the entry is appended only if missing.

## Idempotent

Running `init` multiple times is safe:
- Existing config.json is overwritten with defaults
- syncs/ directory created if missing
- `.gitignore` updated only when needed

## Output

```
Created .doctrack/
```

## Implementation

Uses `init_doctrack()` from config module:
1. Create .doctrack/ directory
2. Write config.json with defaults
3. Create syncs/ subdirectory
4. Write .gitignore in syncs/

---

related docs:
- docs/concepts.md             - Config type
- docs/guides/setup-project.md - project setup guide

related sources:
- src/doctrack/commands/init.py  - init command
- src/doctrack/core/config.py    - init_doctrack function
- src/doctrack/core/constants.py - default config values
