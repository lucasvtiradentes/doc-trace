# Rules

## Design Principles

### Single-Responsibility Commands

Each command does one thing:
- `check`   - validates refs
- `cascade` - finds affected docs
- `prompt`  - generates AI tasks
- `tree`    - shows dependencies
- `init`    - creates config

### Explicit Paths from Repo Root

All paths in metadata are relative to repository root, not the doc file.

```
related sources:
- src/module.py          ← from repo root
- not ./src/module.py    ← not relative to doc
```

### Doc Metadata-Driven

Validation and cascade rely on doc metadata sections. No magic inference or heuristics.

### Lazy Error Recovery

On parse errors in `check`, report the doc error and continue scanning other docs. The command still exits non-zero when any error exists.

## Code Conventions

### Future Annotations

All command/core modules use:

```python
from __future__ import annotations
```

Enables forward references and modern type syntax.

### Lowercase CLI

Commands are lowercase, no hyphens:
- `check`, `cascade`, `prompt`, `tree`, `init`

### Path-Based Abstractions

Use `pathlib.Path` everywhere, not string paths.

### NamedTuple for Results

Return types are NamedTuples for clear structure:
- `RefEntry`
- `ParsedDoc`
- `CascadeResult`
- `DependencyTree`

### Iterator Patterns

`check_refs()` yields results one at a time instead of building full list.

## Anti-Patterns to Avoid

### Exhaustive Dependency Crawling

Do not recursively follow all refs without limits. Use `cascade_depth_limit`.

### Committing lock.json

`lock.json` is stored in `.docsync/lock.json` and used by incremental prompt generation.

### Hardcoded Doc Paths

Pass paths as arguments. Do not assume `docs/` location.

### Blocking on Parse Errors

Do not abort the whole scan on first parse error; accumulate errors and fail at the end with exit code `1`.

---

related docs:
- docs/architecture.md - system design context
- docs/concepts.md     - type definitions

related sources:
- src/docsync/commands/ - command implementations
- src/docsync/core/     - core modules
