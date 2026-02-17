# Overview

CLI tool that keeps documentation in sync with code in large codebases. Detects which docs are affected by code changes and validates them using Claude.

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
2. AI tools like Claude Code don't know which files to read to validate each doc

docsync solves this by adding "hints" to each doc - `related sources:` tells Claude exactly what to read.

## Features

- check       - validates all referenced paths exist
- cascade     - finds docs affected by code changes (with directory matching)
- validate    - runs Claude to verify doc content against source code
- parallel    - validates multiple docs simultaneously
- incremental - only validates docs changed since last run

## Commands

```bash
docsync check <path>                   # validate refs exist
docsync cascade <commit> --docs <dir>  # list affected docs
docsync validate <path>                # run claude validation
docsync validate <path> --incremental  # validate only changed docs
docsync init                           # create .docsync.json
```

### Examples

```bash
docsync check docs/                    # check all docs in docs/
docsync cascade HEAD~5 --docs docs/    # docs affected by last 5 commits
docsync cascade abc123 --docs docs/    # docs affected since commit abc123
docsync validate docs/ --incremental   # validate only what changed
```

Exit codes: 0 = ok, 1 = issues found, 2 = config error.

## Configuration

Create `.docsync.json` in your repo root:

```json
{
  "ignored_paths": [
    "**/migrations/**",
    "**/*.test.ts"
  ],
  "cascade_depth_limit": null,
  "validation": {
    "parallel_agents": 3,
    "timeout_per_doc": 120
  }
}
```

## Install

```bash
pipx install docsync
# pip install docsync
```

## Development

```bash
make install        # create venv + install
make check          # lint
make test           # run tests
docsync check docs/ # practical test
```
