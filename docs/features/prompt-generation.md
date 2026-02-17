# Prompt Generation (prompt command)

Generates structured AI review tasks for documentation.

## Usage

```bash
docsync prompt docs/
docsync prompt docs/ --parallel
docsync prompt docs/ --incremental
docsync prompt docs/ --update-lock
```

## Options

| Flag          | Description                              |
|---------------|------------------------------------------|
| --parallel    | ignore dependencies, flat list           |
| --incremental | only docs changed since last commit      |
| --update-lock | save current commit to lock.json         |

## Default Behavior (Ordered)

Groups docs by dependency level for sequential processing:

```
Phase 1 - Independent (launch parallel):
  docs/concepts.md
    sources: src/core/types.py
  docs/utils.md
    sources: src/utils/

Phase 2 - Level 1 (after phase 1 completes):
  docs/api.md
    sources: src/api.py
```

- Phase 1:  docs with no `related docs:` references
- Phase 2+: docs depending on previous phase docs

## Parallel Mode

Outputs flat list without dependency ordering:

```
1. docs/concepts.md
   sources: src/core/types.py

2. docs/utils.md
   sources: src/utils/

3. docs/api.md
   sources: src/api.py
   related docs: docs/concepts.md
```

## Incremental Mode

Only includes docs affected since last analyzed commit.

1. Loads `last_analyzed_commit` from lock.json
2. Runs cascade analysis from that commit
3. Filters doc list to affected docs only

If no lock file or no previous commit, includes all docs.

## Update Lock

With `--update-lock`, saves current commit hash to `.docsync/lock.json`:

```json
{
  "last_analyzed_commit": "abc123...",
  "last_run": "2024-01-15T10:30:00+00:00"
}
```

## Custom Templates

Create `.docsync/prompt.md` to customize output format.

Template variables:
- `{count}`     - number of docs
- `{docs}`      - formatted doc list
- `{syncs_dir}` - output directory path

## Output Directory

Generated prompts reference `.docsync/syncs/<timestamp>/` for AI to store results.

---

related docs:
- docs/features/cascade.md         - cascade used for incremental mode
- docs/features/dependency-tree.md - dependency level computation
- docs/concepts.md                 - Lock type

related sources:
- src/docsync/commands/prompt.py - prompt generation
- src/docsync/core/lock.py       - lock file handling
- src/docsync/prompts/prompt.md  - default template
