# Concepts

## Core Types

### RefEntry

Reference tuple extracted from doc metadata sections.

| Field       | Type | Description                   |
|-------------|------|-------------------------------|
| path        | str  | relative path from repo root  |
| description | str  | human-readable description    |
| line_number | int  | line number in source doc     |

### ParsedDoc

Container for extracted references from a markdown file.

| Field           | Type            | Description              |
|-----------------|-----------------|--------------------------|
| related_docs    | list[RefEntry]  | doc-to-doc references    |
| related_sources | list[RefEntry]  | doc-to-source references |

### CascadeResult

Output from cascade analysis.

| Field         | Type                      | Description                         |
|---------------|---------------------------|-------------------------------------|
| affected_docs | list[Path]                | all docs needing review             |
| direct_hits   | list[Path]                | docs with changed source refs       |
| cascade_hits  | list[Path]                | docs reached via doc-to-doc refs    |
| circular_refs | list[tuple[Path, Path]]   | detected circular dependencies      |

### Config

Runtime configuration loaded from .docsync/config.json.

| Field              | Type           | Default | Description                       |
|--------------------|----------------|---------|-----------------------------------|
| ignored_paths      | list[str]      | []      | fnmatch patterns to skip          |
| cascade_depth_limit| int or None    | None    | max cascade depth (None=unlimited)|

### CheckResult

Validation result for a single doc.

| Field    | Type           | Description                  |
|----------|----------------|------------------------------|
| doc_path | Path           | path to the validated doc    |
| errors   | list[RefError] | list of validation errors    |
| ok       | property       | True if no errors            |

### RefError

Single validation error.

| Field    | Type     | Description                    |
|----------|----------|--------------------------------|
| doc_path | Path     | doc containing the bad ref     |
| ref      | RefEntry | the problematic reference      |
| message  | str      | error description              |

### Lock

State tracking for incremental mode.

| Field                | Type         | Description                      |
|----------------------|--------------|----------------------------------|
| last_analyzed_commit | str or None  | commit hash from last run        |
| last_run             | str or None  | ISO timestamp of last run        |
| docs_validated       | list[str]    | paths validated in last run      |

### DependencyTree

Dependency graph analysis result.

| Field    | Type                    | Description                      |
|----------|-------------------------|----------------------------------|
| levels   | list[list[Path]]        | topological tiers (0=independent)|
| circular | list[tuple[Path, Path]] | detected circular refs           |
| doc_deps | dict[Path, list[Path]]  | direct dependencies per doc      |

## Terminology

### Direct Hit

A doc is a "direct hit" when one of its `related sources:` paths appears in the git diff. These docs directly reference changed code.

### Cascade Hit

A doc is a "cascade hit" when it references (via `related docs:`) another doc that was affected. Cascade hits propagate through the dependency graph.

### Circular Dependency

Occurs when doc A references doc B and doc B references doc A (directly or through intermediate docs). Detected and warned, but does not block processing.

### Dependency Level

- Level 0: docs with no `related docs:` references (independent)
- Level N: docs whose deepest dependency is at level N-1

### Metadata Section

The portion of a markdown file after the `---` separator containing `related docs:` and `related sources:` lists.

```
# Doc Title

Content here...

---

related docs:
- docs/other.md - description

related sources:
- src/module.py - description
```

---

related docs:
- docs/architecture.md     - how types flow through system
- docs/features/cascade.md - cascade algorithm using these types

related sources:
- src/docsync/core/parser.py      - RefEntry, ParsedDoc definitions
- src/docsync/commands/cascade.py - CascadeResult definition
- src/docsync/commands/check.py   - CheckResult, RefError definitions
- src/docsync/commands/tree.py    - DependencyTree definition
- src/docsync/core/config.py      - Config definition
- src/docsync/core/lock.py        - Lock definition
