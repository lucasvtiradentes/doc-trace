---
title: Repository Structure
description: Directory layout and file organization
related_docs:
  - docs/repo/tooling.md: dev tools configuration
  - docs/testing.md: test patterns and coverage
sources:
  - src/doctrace/: main package
  - tests/: test suite
  - .github/workflows/: CI pipelines
---

# Repository Structure

```
doc-sync/
├── src/doctrace/           ← main package
│   ├── __init__.py
│   ├── cli.py             ← entry point, argparse setup
│   ├── commands/          ← subcommand implementations
│   │   ├── __init__.py
│   │   ├── info.py        ← info command (phases + validation)
│   │   ├── affected.py    ← change detection + output formatting
│   │   ├── preview/       ← interactive browser UI module
│   │   │   ├── __init__.py
│   │   │   ├── server.py  ← HTTP server + run()
│   │   │   ├── tree.py    ← dependency tree logic
│   │   │   ├── graph.py   ← graph data building
│   │   │   ├── search.py  ← doc content search
│   │   │   └── template.html ← HTML/JS template
│   │   ├── lock.py        ← lock state management
│   │   └── init.py        ← project initialization
│   └── core/              ← shared logic
│       ├── __init__.py
│       ├── docs.py        ← doc parsing + indexing
│       ├── config.py      ← config loading/validation
│       ├── lock.py        ← state persistence
│       ├── git.py         ← git operations
│       └── constants.py   ← shared constants
├── tests/                 ← pytest test suite
│   ├── __init__.py
│   ├── affected/          ← affected tests
│   ├── validate/          ← validation tests
│   ├── config/            ← config validation tests
│   ├── parser/            ← parser tests
│   ├── preview/           ← preview tests
│   └── cli/               ← CLI argument tests
├── docs/                  ← documentation
├── .github/workflows/     ← CI/CD pipelines
│   ├── prs.yml            ← PR checks
│   ├── push-to-main.yml   ← main branch checks
│   ├── callable-ci.yml    ← reusable CI workflow
│   └── release.yml        ← PyPI release workflow
├── .changelog/            ← towncrier fragments
├── pyproject.toml         ← project config, deps
├── Makefile               ← dev commands
└── README.md
```

## Key Directories

### src/doctrace/commands/

Each file implements one CLI subcommand. All follow the same pattern:
- Define command-specific types
- Implement core logic
- Export `run()` function called by cli.py

### src/doctrace/core/

Shared modules used across commands:
- `docs.py`      - doc parsing, indexing, dependency tree
- `config.py`    - loads and validates config.json
- `lock.py`      - manages lock.json state
- `git.py`       - git operations, change detection
- `constants.py` - file/dir names, default values

### tests/

Pytest tests grouped by feature area. Most tests use temporary directories and fixture docs copied from local test fixtures.

