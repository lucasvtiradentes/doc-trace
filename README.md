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
- prompt  - generates prompt for parallel AI validation (provider-agnostic)
- report  - generates JSON with docs + sources

## Commands

```bash
docsync check <path>                   # validate refs exist
docsync cascade <commit> --docs <dir>  # list affected docs
docsync prompt <path>                  # generate prompt for AI validation
docsync prompt <path> --incremental    # only include changed docs
docsync prompt <path> --json           # output as JSON for scripts
docsync init                           # create .docsync/ folder
```

### Examples

```bash
docsync check docs/                    # check all docs in docs/
docsync cascade HEAD~5 --docs docs/    # docs affected by last 5 commits
docsync prompt docs/ | pbcopy          # copy prompt to clipboard
```

### AI Validation

The `prompt` command generates a prompt that tells the AI to launch parallel agents:

```
Validate 5 docs by launching PARALLEL agents (one per doc).

For each doc, launch a subagent that will:
1. Read the doc file
2. Read all its related sources
3. Check if the doc content accurately describes the source code
4. Report any outdated, incorrect, or missing information

IMPORTANT: Launch ALL agents in a SINGLE message for parallel execution.

Docs to validate:

1. docs/bookings.md
   sources: src/booking/, src/booking/commands/
   related docs: docs/payments.md
...
```

Use with any AI:
```bash
docsync prompt docs/ | pbcopy          # paste into any AI chat
claude "$(docsync prompt docs/)"       # direct to Claude Code
```

Exit codes: 0 = ok, 1 = issues found.

## Configuration

Run `docsync init` to create the `.docsync/` folder:

```
.docsync/
├── config.json   # required
├── prompt.md     # optional - custom prompt template
└── lock.json     # optional - created by --incremental
```

### config.json

```json
{
  "ignored_paths": [
    "**/migrations/**",
    "**/*.test.ts"
  ],
  "cascade_depth_limit": null
}
```

### prompt.md (optional)

Custom prompt template with placeholders:

```markdown
Validate {count} docs in PORTUGUESE.

Launch parallel agents (one per doc).

Each agent should:
1. Read the doc
2. Read related sources
3. Report issues in Portuguese

{docs_list}
```

Placeholders:
- `{count}` - number of docs
- `{docs_list}` - formatted list of docs with sources

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
