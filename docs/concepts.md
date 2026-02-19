---
title: Concepts
description: Core types and terminology
sources:
  - src/doctrace/core/parser.py: RefEntry, ParsedDoc definitions
  - src/doctrace/commands/affected.py: AffectedResult definition
  - src/doctrace/commands/validate.py: ValidateResult, RefError definitions
  - src/doctrace/core/config.py: Config definition
  - src/doctrace/core/lock.py: Lock definition
  - src/doctrace/core/git.py: FileChange, CommitInfo definitions
---

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

| Field         | Type           | Description                              |
|---------------|----------------|------------------------------------------|
| required_docs | list[RefEntry] | hard deps, used for propagation + phases |
| related_docs  | list[RefEntry] | soft refs, informational only            |
| sources       | list[RefEntry] | code references                          |

### AffectedResult

Output from affected analysis.

| Field            | Type                      | Description                              |
|------------------|---------------------------|------------------------------------------|
| affected_docs    | list[Path]                | all docs needing review                  |
| direct_hits      | list[Path]                | docs with changed source refs            |
| indirect_hits    | list[Path]                | docs reached via doc-to-doc refs         |
| circular_refs    | list[tuple[Path, Path]]   | detected circular dependencies           |
| matches          | dict[str, list[Path]]     | changed source paths to affected docs    |
| indirect_chains  | dict[Path, Path]          | indirect hit doc to doc it was reached through |

### Config

Runtime configuration loaded from .doctrace/config.json.

| Field               | Type           | Default | Description                           |
|---------------------|----------------|---------|---------------------------------------|
| ignored_paths       | list[str]      | []      | fnmatch patterns to skip              |
| affected_depth_limit| int or None    | None    | max propagation depth (None=unlimited)|
| metadata            | MetadataConfig | defaults| metadata parsing settings             |

### MetadataConfig

Settings for how doc metadata is parsed.

| Field             | Type | Default         | Description                          |
|-------------------|------|-----------------|--------------------------------------|
| required_docs_key | str  | "required_docs" | header for required doc refs section |
| related_docs_key  | str  | "related_docs"  | header for related doc refs section  |
| sources_key       | str  | "sources"       | header for source references section |

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

## Terminology

### Direct Hit

A doc is a "direct hit" when one of its `sources:` paths appears in the git diff. These docs directly reference changed code.

### Indirect Hit

A doc is an "indirect hit" when it references (via `required_docs:`) another doc that was affected. Indirect hits propagate through the dependency graph based on required_docs only (not related_docs).

### Circular Dependency

Occurs when docs reference each other in a cycle. Commands detect this and continue processing; warnings/recorded pairs are non-blocking.

### Metadata Section

YAML frontmatter at the top of the document:

```
---
title: Doc Title
description: Brief description
required_docs:
  - docs/dependency.md: needed to understand this doc
related_docs:
  - docs/related.md: related but not required
sources:
  - src/module.py: code implementation
---

# Doc Title

Content here...
```

