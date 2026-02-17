# Overview

CLI tool that keeps documentation in sync with code in large codebases. Detects which docs are affected by code changes and generates reports for AI validation.

```
  src/booking/handler.ts changed
            │
            v
  ┌─────────────────────────┐
  │ docsync cascade HEAD~1  │
  └───────────┬─────────────┘
              │
              v
  ┌─────────────────────────┐      ┌─────────────────────────┐
  │ Direct hits:            │      │ docs/bookings.md        │
  │  - docs/bookings.md     │ ──>  │                         │
  └─────────────────────────┘      │ related sources:        │
              │                    │  - src/booking/  <───── │ ← matched!
              v                    └─────────────────────────┘
  ┌─────────────────────────┐
  │ Cascade hits:           │      docs/bookings.md references
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
docsync cascade HEAD~1

Direct hits (1):
  docs/bookings.md       <- references src/booking/

Cascade hits (1):
  docs/payments.md       <- referenced BY docs/bookings.md
```

The cascade propagates: if `bookings.md` might be outdated, then `payments.md` (which references it) might also need review.

</details>

## Motivation

In large codebases, docs get outdated because:
1. No one remembers which docs need updating when a file changes
2. AI agents don't know which files to read to validate each doc

docsync solves this by adding "hints" to each doc - `related sources:` tells any AI exactly what to read.

## Features

- check   - validates all referenced paths exist
- cascade - finds docs affected by code changes (with directory matching)
- sync    - generates prompt for AI to fix docs (ordered by deps)
- tree    - shows doc dependency tree

## Quickstart

### 1. Install

```bash
pipx install docsync
```

### 2. Add metadata to your docs

Each doc needs two sections at the end (after a `---` separator):

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

### 3. Initialize config (optional)

```bash
docsync init    # creates .docsync/ folder
```

<details>
<summary>Config options</summary>

```
.docsync/
├── config.json   # required
├── sync.md       # optional - custom prompt template
├── lock.json     # optional - tracks last synced commit
└── syncs/        # ignored - AI writes sync reports here
```

config.json:
```json
{
  "ignored_paths": ["**/migrations/**", "**/*.test.ts"],
  "cascade_depth_limit": null
}
```

sync.md (custom template):
```markdown
Sync {count} docs. Write reports to {syncs_dir}/

{phases}
```

Placeholders: `{count}`, `{phases}`, `{docs_list}`, `{syncs_dir}`

</details>

### 4. Validate your setup

```bash
docsync check docs/    # ensures all paths exist
```

### 5. Use it

```bash
docsync cascade HEAD~5 --docs docs/    # docs affected by last 5 commits
docsync sync docs/ | pbcopy            # generate AI prompt
claude "$(docsync sync docs/)"         # or pipe directly to AI
```

## Commands

```bash
docsync check <path>                   # validate refs exist
docsync cascade <commit> --docs <dir>  # list affected docs
docsync sync <path>                    # generate prompt (ordered by deps)
docsync sync <path> --parallel         # ignore deps, all at once
docsync sync <path> --incremental      # only include changed docs
docsync sync <path> --update-lock      # update lock.json after sync
docsync sync <path> --json             # output as JSON for scripts
docsync tree <path>                    # show doc dependency tree
docsync init                           # create .docsync/ folder
docsync --version                      # show version
```

### AI Sync

The `sync` command generates a prompt for AI to fix docs in phases (respecting dependencies):

```
Sync 5 docs by launching agents in phases (respecting dependencies).

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

Use `--parallel` to ignore dependencies and sync all at once.

## Development

```bash
make install        # create venv + install
make check          # lint
make test           # run tests
docsync check docs/ # practical test
```
