---
title: Architecture
description: System design, data flow, and module structure
required_docs:
  - docs/concepts.md: key types used in data flow
related_docs:
  - docs/features/affected.md:   affected algorithm details
  - docs/features/validation.md: validate command details
  - docs/features/preview.md:    preview command details
sources:
  - src/doctrace/cli.py:    entry point and dispatcher
  - src/doctrace/commands/: command implementations
  - src/doctrace/core/:     core modules
---

## Entry Point

`cli.py:main()` parses arguments and dispatches to subcommand handlers.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                  cli.py:main()                                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│  argparse → subcommand dispatcher                                                │
│                                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌──────┐ ┌───────┐ ┌────────────┐         │
│  │   info   │ │ affected │ │ preview │ │ init │ │ index │ │ completion │         │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ └──┬───┘ └───┬───┘ └─────┬──────┘         │
│       │            │            │         │         │            │               │
│       v            v            v         v         v            v               │
│  commands/    commands/    commands/  commands/ commands/    commands/            │
│  info.py     affected.py  preview/   init.py   index.py    completion.py         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Module Structure

```
src/doctrace/
├── cli.py              ← entry point, arg parsing
├── cmd_registry.py     ← centralized command metadata
├── commands/
│   ├── info.py         ← info command (phases + validation)
│   ├── affected.py     ← change detection + output formatting
│   ├── preview/        ← interactive browser UI module
│   ├── init.py         ← project setup
│   ├── index.py        ← index generation from frontmatter
│   └── completion.py   ← shell autocompletion
├── core/
│   ├── docs.py         ← doc parsing + indexing
│   ├── config.py       ← runtime configuration
│   ├── git.py          ← git operations
│   ├── constants.py    ← shared constants
│   └── filtering.py    ← fnmatch-based ignore filtering
```

## Data Flow - Info Command

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
docs/*.md → build_doc_index()                       │
                   │         (core/docs.py)         │
       ┌───────────┴───────────┐                   │
       v                       v                   │
source_to_docs           reverse_deps              │
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
       (BFS traversal)
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
Input: initial_docs, doc_to_docs
Output: indirect_hits, circular_refs, indirect_chains

visited = set(initial_docs)
current_level = set(initial_docs)

while current_level not empty:
    next_level = empty set

    for each doc in current_level:
        for each referencing_doc in doc_to_docs[doc]:
            if referencing_doc in visited:
                continue
            add to visited
            add to indirect_hits
            add to next_level

    current_level = next_level

circular_refs = _find_circular_refs(visited, doc_to_docs)
```

## Observability

| Signal   | Description                           |
|----------|---------------------------------------|
| Exit 0   | success, no errors                    |
| Exit 1   | validation errors found               |
| Exit 2   | scope error (affected command)        |
| stdout   | results output                        |
| Warnings | circular ref detection (non-blocking) |

## Config Loading

```
find_config(start_path):
    current = start_path
    while current != root:
        if doctrace.json exists:
            return config_path
        current = parent
    return None
```

