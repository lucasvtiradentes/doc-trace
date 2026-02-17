# Initialization (init command)

Creates the .docsync/ configuration directory.

## Usage

```bash
docsync init
```

## What It Creates

```
.docsync/
├── config.json     ← default configuration
└── syncs/          ← AI sync report storage
    └── .gitignore  ← ignore sync outputs
```

## Default config.json

```json
{
  "ignored_paths": [],
  "cascade_depth_limit": null
}
```

| Field              | Default | Description                    |
|--------------------|---------|--------------------------------|
| ignored_paths      | []      | patterns to skip in validation |
| cascade_depth_limit| null    | max cascade depth (unlimited)  |

## syncs/ Directory

Storage for AI-generated sync reports.

The `.gitignore` ignores all files except itself:

```
*
!.gitignore
```

This keeps sync outputs local and untracked.

## Idempotent

Running `init` multiple times is safe:
- Existing config.json is overwritten with defaults
- syncs/ directory created if missing
- .gitignore recreated

## Output

```
Created .docsync/
```

## Implementation

Uses `init_docsync()` from config module:
1. Create .docsync/ directory
2. Write config.json with defaults
3. Create syncs/ subdirectory
4. Write .gitignore in syncs/

---

related docs:
- docs/concepts.md             - Config type
- docs/guides/setup-project.md - project setup guide

related sources:
- src/docsync/commands/init.py  - init command
- src/docsync/core/config.py    - init_docsync function
- src/docsync/core/constants.py - default config values
