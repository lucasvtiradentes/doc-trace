# Overview

CLI tool that keeps documentation in sync with code in large codebases. Detects which docs are affected by code changes.

```
  src/booking/handler.ts changed
              │
              ▼
  ┌───────────────────────────────────┐
  │ docsync affected docs/ --last 1   │
  └───────────────────────────────────┘
              │
              ▼
  ┌───────────────────────────────────┐
  │ Direct hits:                      │
  │   docs/bookings.md                │  ← has "related sources: src/booking/"
  │                                   │
  │ Indirect hits:                    │
  │   docs/payments.md                │  ← referenced BY docs/bookings.md
  └───────────────────────────────────┘
```

<details>
<summary>How it works</summary>

Each doc ends with metadata sections:

```markdown
# Booking System

How bookings work...

---

related docs:
- docs/payments.md - payment integration

related sources:
- src/booking/           - booking module
- src/booking/commands/  - command handlers
```

When `src/booking/handler.ts` changes:

```
docsync affected docs/ --last 1

Direct hits (1):
  docs/bookings.md       <- references src/booking/

Indirect hits (1):
  docs/payments.md       <- referenced BY docs/bookings.md
```

The propagation: if `bookings.md` might be outdated, then `payments.md` (which references it) might also need review.

</details>

<details>
<summary>Interactive preview explorer</summary>

![Preview](.github/images/preview.png)

</details>

## Features

- validate - validates all referenced paths exist
- affected - finds docs affected by code changes (with dependency ordering)
- preview  - interactive docs explorer in browser
- lock     - manages lock state for incremental analysis

## Motivation

In large codebases, docs get outdated because:
1. No one remembers which docs need updating when a file changes
2. AI agents don't know which files to read to validate each doc

docsync solves this by adding "hints" to each doc - `related sources:` tells any AI exactly what to read.

## Quickstart

### 1. Install

```bash
pipx install docsync
```

### 2. Add metadata to your docs

<details>
<summary>Custom style (default) - metadata at bottom</summary>

```markdown
# My Feature

Documentation content here...

---

related docs:
- docs/other-feature.md - brief description

related sources:
- src/feature/           - main module
- src/feature/utils.ts   - helper functions
```

</details>

<details>
<summary>Frontmatter style - metadata at top</summary>

```markdown
---
related docs:
  - docs/other-feature.md - brief description

related sources:
  - src/feature/         - main module
  - src/feature/utils.ts - helper functions
---

# My Feature

Documentation content here...
```

Config required:
```json
{
  "metadata": {
    "style": "frontmatter"
  }
}
```

</details>

### 3. Initialize config (optional)

```bash
docsync init    # creates .docsync/ folder
```

<details>
<summary>Config options</summary>

```
.docsync/
├── config.json   # required
├── lock.json     # tracks last analyzed commit
└── syncs/        # output directory (added to .gitignore)
```

config.json:
```json
{
  "ignored_paths": ["**/migrations/**", "**/*.test.ts"],
  "affected_depth_limit": null,
  "metadata": {
    "style": "custom",
    "docs_key": "related docs",
    "sources_key": "related sources",
    "require_separator": true
  }
}
```

metadata options:
- `style`:             "frontmatter" (YAML at top) or "custom" (flexible format)
- `docs_key`:          header for doc references (default: "related docs")
- `sources_key`:       header for source references (default: "related sources")
- `require_separator`: if true, only parse after `---` (default: true, custom only)

</details>

### 4. Use it

```bash
docsync validate docs/                     # validate all refs exist
docsync affected docs/ --last 5            # find docs affected by last 5 commits
docsync affected docs/ --since v1.0.0      # find docs affected since tag/commit/branch
docsync preview docs/                      # interactive explorer in browser
```

<details>
<summary>All commands</summary>

| Command                                          | Description                          |
|--------------------------------------------------|--------------------------------------|
| `docsync validate <path>`                        | validate refs exist                  |
| `docsync affected <path> --last <N>`             | list affected docs by last N commits |
| `docsync affected <path> --since <ref>`          | list affected docs since ref         |
| `docsync affected <path> --since-lock`           | list affected docs since lock commit |
| `docsync affected <path> --base-branch <branch>` | list affected docs from merge-base   |
| `docsync affected <path> --verbose`              | show changed files and match details |
| `docsync affected <path> --json`                 | output as JSON                       |
| `docsync preview <path>`                         | interactive explorer in browser      |
| `docsync preview <path> --port <N>`              | preview on custom port (default 8420)|
| `docsync lock update`                            | save current commit to lock.json     |
| `docsync lock show`                              | show lock.json state                 |
| `docsync init`                                   | create .docsync/ folder              |
| `docsync --version`                              | show version                         |

</details>

<details>
<summary>Example output</summary>

```
Direct hits (3):
  docs/concepts.md
  docs/api.md
  docs/utils.md

Indirect hits (1):
  docs/overview.md <- docs/api.md

Phases (3):
  1. docs/concepts.md, docs/utils.md
  2. docs/api.md
  3. docs/overview.md
```

Phases show dependency order - useful for AI agents processing docs.

</details>

## Development

```bash
make install           # create venv + install
make check             # lint
make test              # run tests
docsync validate docs/ # practical test
```

```bash
# dev alias (docsyncd)
ln -s $(pwd)/.venv/bin/docsync ~/.local/bin/docsyncd   # install
rm ~/.local/bin/docsyncd                                # remove
```
