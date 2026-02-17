# Architecture

## Entry Point

`cli.py:main()` parses arguments and dispatches to subcommand handlers.

```
┌─────────────────────────────────────────────────────────────┐
│                        cli.py:main()                        │
├─────────────────────────────────────────────────────────────┤
│  argparse → subcommand dispatcher                           │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌──────┐ ┌──────┐    │
│  │ validate │ │ affected │ │ preview │ │ lock │ │ init │    │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ └──┬───┘ └──┬───┘    │
│       │            │            │         │        │        │
│       v            v            v         v        v        │
│  commands/    commands/    commands/  commands/ commands/   │
│  validate.py  affected.py  preview.py lock.py   init.py     │
└─────────────────────────────────────────────────────────────┘
```

## Module Structure

```
src/doctrack/
├── cli.py              ← entry point, arg parsing
├── commands/
│   ├── validate.py     ← ref validation
│   ├── affected.py     ← change detection + output formatting
│   ├── preview/        ← interactive browser UI module
│   ├── lock.py         ← lock state management
│   └── init.py         ← project setup
├── core/
│   ├── parser.py       ← doc metadata extraction
│   ├── config.py       ← runtime configuration
│   ├── lock.py         ← lock state persistence
│   ├── git.py          ← git operations
│   └── constants.py    ← shared constants
```

## Data Flow - Validate Command

```
docs/*.md → parse_doc() → RefEntry list (path, line)
                              │
                              v
                        validate_refs()
                              │
              ┌───────────────┴───────────────┐
              v                               v
       Path exists?                    Glob matches?
       repo_root / ref                 (for wildcards)
              │                               │
              └───────────────┬───────────────┘
                              v
                        ValidateResult
                   (doc_path, errors[])
```

## Data Flow - Affected Command

```
git diff <commit> → get_changed_files() → changed_files (list[str])
                    (core/git.py)                  │
docs/*.md → _build_indexes()                       │
                   │                               │
       ┌───────────┴───────────┐                   │
       v                       v                   │
source_to_docs           doc_to_docs               │
{path: [docs]}           {doc: [docs]}             │
       │                       │                   │
       └───────────┬───────────┘                   │
                   v                               │
                   ←───────────────────────────────┘
                   │
                   v
       _find_direct_hits() → direct_hits (docs with changed source refs)
                                    │
                                    v
       _propagate() → indirect_hits, circular_refs, indirect_chains
       (BFS traversal, depth_limit)
                                    │
                                    v
                            AffectedResult
              (affected, direct, indirect, circular, matches, indirect_chains)
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    v                               v
              default output                  --json
           (phases always shown)           (JSON output)
```

## Propagation Algorithm (BFS)

```
Input: initial_docs, doc_to_docs, depth_limit
Output: indirect_hits, circular_refs, indirect_chains

visited = set(initial_docs)
current_level = set(initial_docs)
depth = 0

while current_level not empty:
    if depth_limit reached:
        break

    next_level = empty set

    for each doc in current_level:
        for each referencing_doc in doc_to_docs[doc]:
            if referencing_doc in visited:
                if not in initial_docs:
                    record circular ref
                continue
            add to visited
            add to indirect_hits
            add to next_level

    current_level = next_level
    depth += 1
```

## Observability

| Signal    | Description                                |
|-----------|--------------------------------------------|
| Exit 0    | success, no errors                         |
| Exit 1    | validation errors found                    |
| Exit 2    | scope error (affected command)             |
| stdout    | results output                             |
| Warnings  | circular ref detection (non-blocking)      |

## Config Loading

```
find_config(start_path):
    current = start_path
    while current != root:
        if .doctrack/config.json exists:
            return config_path
        current = parent
    return None
```

---

related docs:
- docs/concepts.md             - key types used in data flow
- docs/features/affected.md    - affected algorithm details
- docs/features/validation.md  - validate command details
- docs/features/preview.md     - preview command details

related sources:
- src/doctrack/cli.py    - entry point and dispatcher
- src/doctrack/commands/ - command implementations
- src/doctrack/core/     - core modules
