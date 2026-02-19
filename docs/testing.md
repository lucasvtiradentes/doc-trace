---
title: Testing
description: Testing strategy and patterns
related_docs:
  - docs/repo/tooling.md: pytest configuration
  - docs/repo/cicd.md: CI test jobs
sources:
  - tests/affected/: affected tests
  - tests/parser/: parser tests
  - tests/preview/: preview tests
  - tests/validate/: validation tests
  - tests/config/: config tests
  - tests/cli/: CLI tests
---

# Testing

## Framework

Pytest configured in `pyproject.toml`:

- `testpaths = ["tests"]`
- `python_files = ["test.py", "test_*.py"]`

Run tests:

```bash
make test
# or
.venv/bin/pytest -v
```

## Test Layout

Tests are organized by feature area:

| Directory / File   | Coverage                                                         |
|--------------------|------------------------------------------------------------------|
| `tests/affected/`  | index building, direct hits, propagation, depth limits, scope resolution |
| `tests/validate/`  | valid refs, missing docs, missing sources                        |
| `tests/config/`    | config validation (valid + invalid)                              |
| `tests/parser/`    | custom/frontmatter parsing, code blocks, line numbers            |
| `tests/preview/`   | dependency tree, search, graph building                          |
| `tests/cli/`       | CLI argument parsing and command dispatch                        |

## Common Patterns

### Temporary directories

Tests create isolated repos/workspaces with `tempfile.TemporaryDirectory()`.

### Fixture-style test data

Many tests copy fixture docs with `shutil.copytree(...)` from nearby `docs/` folders.

### Mocked change detection

Affected tests patch change input (for example `get_changed_files`) to avoid relying on real git history.

## CI-Relevant Commands

Local equivalents of CI jobs:

```bash
make check          # ruff check + ruff format --check
make test           # pytest -v
make practical-test # doctrace info docs/
```

