# Initialization (init command)

Creates the .doctrace/ configuration directory.

## Usage

```bash
doctrace init
```

## What It Creates

```
.doctrace/
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
.doctrace/syncs/
```

If `.gitignore` already exists, the entry is appended only if missing.

## Idempotent

Running `init` multiple times is safe:
- Existing config.json is overwritten with defaults
- syncs/ directory created if missing
- `.gitignore` updated only when needed

## Output

```
Created .doctrace/
```

## Implementation

Uses `init_doctrace()` from config module:
1. Create .doctrace/ directory
2. Write config.json with defaults
3. Create syncs/ subdirectory
4. Update repo root .gitignore with syncs/ entry

---

related docs:
- docs/concepts.md             - Config type
- docs/guides/setup-project.md - project setup guide

related sources:
- src/doctrace/commands/init.py  - init command
- src/doctrace/core/config.py    - init_doctrace function
- src/doctrace/core/constants.py - default config values
