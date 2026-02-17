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
| --incremental | only docs affected since locked commit   |
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

Includes docs affected since `lock.json:last_analyzed_commit`.

1. Loads `last_analyzed_commit` from lock.json
2. Runs affected analysis from that commit (`find_affected_docs`)
3. Filters doc list to affected docs (direct hits + indirect hits)

If no lock file or no previous commit, includes all docs.

## Update Lock

With `--update-lock`, saves current commit hash to `.docsync/lock.json` and updates `last_run`:

```json
{
  "last_analyzed_commit": "abc123...",
  "last_run": "2026-02-17T09:52:01+00:00",
  "docs_validated": []
}
```

## Custom Templates

Create `.docsync/prompt.md` to customize output format.

Template variables:
- `{count}`     - number of docs
- `{docs}`      - formatted doc list
- `{syncs_dir}` - output directory path

## Output Directory

Generated prompts reference `.docsync/syncs/<timestamp>/` with timestamp format `%Y-%m-%dT%H-%M-%S`.

---

related docs:
- docs/features/affected.md        - affected used for incremental mode
- docs/features/dependency-tree.md - dependency level computation
- docs/concepts.md                 - Lock type

related sources:
- src/docsync/commands/prompt.py - prompt generation
- src/docsync/core/lock.py       - lock file handling
- src/docsync/prompts/prompt.md  - default template
