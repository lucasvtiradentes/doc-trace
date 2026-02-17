# Architecture

## Entry Point

`cli.py:main()` parses arguments and dispatches to subcommand handlers.

```
┌─────────────────────────────────────────────────────────────┐
│                        cli.py:main()                        │
├─────────────────────────────────────────────────────────────┤
│  argparse → subcommand dispatcher                           │
│                                                             │
│  ┌─────────┐ ┌─────────┐ ┌────────┐ ┌──────┐ ┌──────┐       │
│  │ check   │ │ cascade │ │ prompt │ │ tree │ │ init │       │
│  └────┬────┘ └────┬────┘ └───┬────┘ └──┬───┘ └──┬───┘       │
│       │           │          │         │        │           │
│       v           v          v         v        v           │
│  commands/   commands/  commands/  commands/ commands/      │
│  check.py    cascade.py prompt.py  tree.py   init.py        │
└─────────────────────────────────────────────────────────────┘
```

## Module Structure

```
src/docsync/
├── cli.py              ← entry point, arg parsing
├── commands/
│   ├── check.py        ← ref validation
│   ├── cascade.py      ← change detection
│   ├── prompt.py       ← AI prompt generation
│   ├── tree.py         ← dependency visualization
│   └── init.py         ← project setup
├── core/
│   ├── parser.py       ← doc metadata extraction
│   ├── config.py       ← runtime configuration
│   ├── lock.py         ← state tracking
│   └── constants.py    ← shared constants
└── prompts/
    └── prompt.md       ← default prompt template
```

## Data Flow - Check Command

```
docs/*.md → parse_doc() → RefEntry list (path, line)
                              │
                              v
                        check_refs()
                              │
              ┌───────────────┴───────────────┐
              v                               v
       Path exists?                    Glob matches?
       repo_root / ref                 (for wildcards)
              │                               │
              └───────────────┬───────────────┘
                              v
                        CheckResult
                   (doc_path, errors[])
```

## Data Flow - Cascade Command

```
git diff <commit> → _get_changed_files() → changed_files (list[str])
                                                   │
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
       _cascade() → cascade_hits, circular_refs
       (BFS traversal, depth_limit)
                                    │
                                    v
                            CascadeResult
                   (affected, direct, cascade, circular)
```

## Cascade Algorithm (BFS)

```
Input: initial_docs, doc_to_docs, depth_limit
Output: cascade_hits, circular_refs

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
            add to cascade_hits
            add to next_level

    current_level = next_level
    depth += 1
```

## Prompt Generation Flow

```
generate_prompt(docs_path, config, incremental, parallel)
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
          v                                       v
   incremental=true                      incremental=false
   load lock.json                        scan all docs
   run cascade from last commit
   filter to affected
          │                                       │
          └───────────────────┬───────────────────┘
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
          v                                       v
   parallel=true                         parallel=false
   flat list output                      _build_sync_levels()
   no dependency order                   topological sort
                                         output phases
```

## Dependency Tree Computation

```
_compute_levels(doc_deps)
│
├── For each doc, recursively compute level:
│
│   doc has no deps? ──yes──→ level = 0 (independent)
│         │
│        no
│         │
│         v
│   level = max(dep_levels) + 1
│
│   circular detection:
│   if doc in visiting set → circular
│
└── Result:
    Level 0: [independent docs]
    Level 1: [docs depending on L0]
    Level 2: [docs depending on L1]
    ...
```

## Observability

| Signal    | Description                                |
|-----------|--------------------------------------------|
| Exit 0    | success, no errors                         |
| Exit 1    | validation errors found                    |
| stdout    | results, prompts, tree output              |
| Warnings  | circular ref detection (non-blocking)      |

## Config Loading

```
find_config(start_path):
    current = start_path
    while current != root:
        if .docsync/config.json exists:
            return config_path
        current = parent
    return None
```

---

related docs:
- docs/concepts.md            - key types used in data flow
- docs/features/cascade.md    - cascade algorithm details
- docs/features/validation.md - check command details

related sources:
- src/docsync/cli.py    - entry point and dispatcher
- src/docsync/commands/ - command implementations
- src/docsync/core/     - core modules
