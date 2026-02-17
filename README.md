# Overview

CLI tool that keeps documentation in sync with code in large codebases. Detects which docs are affected by code changes and generates reports for AI validation.

```
  src/booking/handler.ts changed
            │
            v
  ┌─────────────────────────────┐
  │ docsync affected docs/ --last 1 │
  └───────────┬─────────────────┘
              │
              v
  ┌─────────────────────────┐      ┌─────────────────────────┐
  │ Direct hits:            │      │ docs/bookings.md        │
  │  - docs/bookings.md     │ ──>  │                         │
  └─────────────────────────┘      │ related sources:        │
              │                    │ - src/booking/  <─────  │ ← matched!
              v                    └─────────────────────────┘
  ┌─────────────────────────┐
  │ Indirect hits:          │      docs/bookings.md references
  │  - docs/payments.md     │ ──>  docs/payments.md, so it
  └─────────────────────────┘      might need review too
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

## Motivation

In large codebases, docs get outdated because:
1. No one remembers which docs need updating when a file changes
2. AI agents don't know which files to read to validate each doc

docsync solves this by adding "hints" to each doc - `related sources:` tells any AI exactly what to read.

## Features

- validate - validates all referenced paths exist
- affected - finds docs affected by code changes (with directory matching)
- prompt   - generates prompt for AI to review docs (ordered by deps)
- tree     - shows doc dependency tree

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
  - src/feature/           - main module
  - src/feature/utils.ts   - helper functions
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
├── prompt.md     # optional - custom prompt template
├── lock.json     # optional - tracks last synced commit
└── syncs/        # AI writes sync reports here (added to .gitignore)
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

prompt.md (custom template):
```markdown
Review {count} docs. Write reports to {syncs_dir}/

{docs}
```

Placeholders: `{count}`, `{docs}`, `{syncs_dir}`

</details>

### 4. Use it

```bash
docsync validate docs/                  # validate all refs exist
docsync affected docs/ --last 5         # find docs affected by last 5 commits
docsync prompt docs/ | pbcopy           # generate AI prompt, copy to clipboard
```

<details>
<summary>All commands</summary>

| Command                                          | Description                         |
|--------------------------------------------------|-------------------------------------|
| `docsync --version`                              | show version                        |
| `docsync init`                                   | create .docsync/ folder             |
| `docsync tree <path>`                            | show doc dependency tree            |
| `docsync validate <path>`                        | validate refs exist                 |
| `docsync affected <path> --last <N>`             | list affected docs by last N commits|
| `docsync affected <path> --since-lock`           | list affected docs since lock commit|
| `docsync affected <path> --base-branch <branch>` | list affected docs from merge-base  |
| `docsync prompt <path>`                          | generate prompt (ordered by deps)   |
| `docsync prompt <path> --parallel`               | ignore deps, all at once            |
| `docsync prompt <path> --incremental`            | only include changed docs           |
| `docsync prompt <path> --update-lock`            | update lock.json after prompt       |

</details>

<details>
<summary>Example prompt output</summary>

```
Review 5 docs by launching agents in phases (respecting dependencies).

Each agent will:
1. Read the doc + all related sources
2. Fix any outdated/incorrect content directly in the doc
3. Write a report to .docsync/syncs/2024-01-15T10-30-00/

Phase 1 - Independent (launch parallel):
  docs/utils.md
  docs/config.md

Phase 2 - Level 1 (after phase 1 completes):
  docs/auth.md
    sources: src/auth/

Phase 3 - Level 2 (after phase 2 completes):
  docs/login.md
    sources: src/login/
```

Use `--parallel` to ignore dependencies and prompt all at once.

</details>

## Development

```bash
make install           # create venv + install
make check             # lint
make test              # run tests
docsync validate docs/ # practical test
```
