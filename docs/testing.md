# Testing

## Framework

Pytest with Python version matrix (3.9, 3.12).

```bash
make test           # or
pytest -v
```

## Test Files

| File                | Coverage                              |
|---------------------|---------------------------------------|
| test_cascade.py     | cascade logic, direct/cascade hits    |
| test_parser.py      | metadata extraction, line numbers     |
| test_tree.py        | dependency tree building, levels      |
| test_validator.py   | ref validation, config validation     |

## Patterns

### Temporary Directories

Tests use `tempfile.TemporaryDirectory` for isolation:

```python
def test_something():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        # ... test logic
```

### Mock Git Subprocess

Git operations mocked with `unittest.mock.patch`:

```python
with patch("docsync.commands.cascade._get_changed_files", return_value=["src/changed.py"]):
    result = find_affected_docs(docs_dir, "HEAD~1", config, repo_root=tmppath)
```

### Inline Test Docs

Test markdown written inline for clarity:

```python
doc.write_text("""# Test

related sources:
- src/module.py - impl
""")
```

## Test Categories

### Unit Tests

- Parser extraction
- Config validation
- Individual functions

### Integration Tests

- Full cascade flow
- Full validation flow
- Prompt generation

## CI Testing

### Local Equivalent

```bash
make test
make practical-test   # docsync check docs/
```

### CI Matrix

| Job            | Python | Commands                    |
|----------------|--------|-----------------------------|
| check          | 3.12   | ruff check, ruff format     |
| test           | 3.9    | pytest -v                   |
| test           | 3.12   | pytest -v                   |
| practical-test | 3.12   | docsync check docs/         |

## Coverage Areas

### Cascade Tests

- `_build_indexes`    - source/doc mapping
- `_cascade`          - BFS traversal, depth limit
- `_find_direct_hits` - exact and directory matching
- Circular ref detection

### Parser Tests

- Both sections present
- Empty sections
- Line number preservation

### Tree Tests

- Independent docs (level 0)
- Multi-level dependencies
- Circular dependency detection
- Output formatting

### Validator Tests

- Valid refs
- Missing source/doc detection
- ignored_paths filtering
- Config validation (valid keys, types)
- Prompt generation modes

---

related docs:
- docs/repo/tooling.md - pytest configuration
- docs/repo/cicd.md    - CI test jobs

related sources:
- tests/test_cascade.py   - cascade tests
- tests/test_parser.py    - parser tests
- tests/test_tree.py      - tree tests
- tests/test_validator.py - validation tests
