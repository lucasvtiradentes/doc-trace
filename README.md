# docsync

Auto-validate and update docs in large codebases.

## Installation

```bash
pip install docsync
```

## Usage

```bash
docsync check docs/              # validate all refs exist
docsync cascade HEAD~1           # list docs affected by git diff
docsync validate docs/           # run claude to validate doc content
docsync validate docs/ --incremental  # validate only changed docs
docsync init                     # create .docsync.json template
```

## Doc Format

Docs should end with `related docs:` and `related sources:` sections:

```markdown
---

related docs:
- docs/other.md - brief description

related sources:
- src/module.py - implementation
```
