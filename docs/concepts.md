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

### AffectedResult

Output from affected analysis.

| Field         | Type                      | Description                         |
|---------------|---------------------------|-------------------------------------|
| affected_docs | list[Path]                | all docs needing review             |
| direct_hits   | list[Path]                | docs with changed source refs       |
| indirect_hits | list[Path]                | docs reached via doc-to-doc refs    |
| circular_refs | list[tuple[Path, Path]]   | detected circular dependencies      |

### Config

Runtime configuration loaded from .docsync/config.json.

| Field               | Type           | Default | Description                        |
|---------------------|----------------|---------|----------------------------------- |
| ignored_paths       | list[str]      | []      | fnmatch patterns to skip           |
| affected_depth_limit| int or None    | None    | max propagation depth (None=unlimited)|
| metadata            | MetadataConfig | defaults| metadata parsing settings          |

### MetadataConfig

Settings for how doc metadata is parsed.

| Field             | Type | Default          | Description                              |
|-------------------|------|------------------|------------------------------------------|
| style             | str  | "custom"         | parsing style ("custom" or "frontmatter")|
| docs_key          | str  | "related docs"   | header for doc references section        |
| sources_key       | str  | "related sources"| header for source references section     |
| require_separator | bool | True             | require --- separator before metadata    |

### ValidateResult

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

### Indirect Hit

A doc is an "indirect hit" when it references (via `related docs:`) another doc that was affected. Indirect hits propagate through the dependency graph.

### Circular Dependency

Occurs when docs reference each other in a cycle. Commands detect this and continue processing; warnings/recorded pairs are non-blocking.

### Dependency Level

- Level 0: docs with no `related docs:` references (independent)
- Level N: docs whose deepest dependency is at level N-1

### Metadata Section

By default (`metadata.style = "custom"`), metadata is parsed after the last `---` separator and contains `related docs:` / `related sources:` lists. This is configurable via `.docsync/config.json` (`metadata.style`, keys, separator requirement).

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

related sources:
- src/docsync/core/parser.py        - RefEntry, ParsedDoc definitions
- src/docsync/commands/affected.py  - AffectedResult definition
- src/docsync/commands/validate.py  - ValidateResult, RefError definitions
- src/docsync/commands/tree.py      - DependencyTree definition
- src/docsync/core/config.py        - Config definition
- src/docsync/core/lock.py          - Lock definition
