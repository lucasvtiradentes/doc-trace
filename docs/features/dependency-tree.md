# Dependency Tree (tree command)

Visualizes documentation dependency graph.

## Usage

```bash
docsync tree docs/
```

## Output Format

```
Level 0 - Independent (3):
  docs/concepts.md
  docs/utils.md
  docs/types.md

Level 1 (2):
  docs/api.md
    └── depends on: docs/concepts.md, docs/types.md
  docs/services.md
    └── depends on: docs/utils.md

Level 2 (1):
  docs/overview.md
    └── depends on: docs/api.md, docs/services.md

Circular dependencies (warning):
  docs/a.md <-> docs/b.md
```

## Dependency Levels

| Level | Meaning                                    |
|-------|--------------------------------------------|
| 0     | no `related docs:` references (independent)|
| 1     | depends only on level 0 docs               |
| N     | depends on at least one level N-1 doc      |

## How Levels Are Computed

```
for each doc:
    if no related_docs:
        level = 0
    else:
        level = max(level of each dependency) + 1
```

Recursive computation with memoization. Circular refs detected by tracking visiting set.

## Circular Dependencies

When a cycle is hit during recursive level computation:
- The cycle edge is recorded in `circular`
- That recursive branch returns `-1`
- The current doc falls back to level `0` only if all of its deps are cyclic
- Processing continues (non-blocking warning in output)

In mixed graphs, docs in the same cycle can end up with different computed levels depending on traversal.

## Use Cases

- Understand doc organization
- Find docs that need review first (level 0)
- Identify circular dependencies to fix
- Plan documentation updates

## Implementation

| Function                 | Purpose                           |
|--------------------------|-----------------------------------|
| build_dependency_tree()  | main entry, returns DependencyTree|
| _build_doc_dependencies()| parse all docs, build dep map     |
| _compute_levels()        | recursive level assignment        |
| format_tree()            | render output string              |

Notes from implementation:
- Docs that fail `parse_doc(...)` are skipped.
- Only `related docs:` references that exist on disk are included as dependencies.

---

related docs:
- docs/concepts.md                   - DependencyTree type
- docs/features/prompt-generation.md - uses levels for phase ordering

related sources:
- src/docsync/commands/tree.py - tree implementation
