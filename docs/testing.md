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

| Directory / File | Coverage |
|------------------|----------|
| `tests/cascade/` | index building, direct hits, cascade traversal, depth limits |
| `tests/check/`   | valid refs, missing docs, missing sources |
| `tests/config/`  | config validation (valid + invalid) |
| `tests/parser/`  | custom/frontmatter parsing, code blocks, line numbers |
| `tests/prompt/`  | ordered output, parallel output, empty docs behavior |
| `tests/tree/`    | independent docs, dependency levels, circular refs, formatting |

## Common Patterns

### Temporary directories

Tests create isolated repos/workspaces with `tempfile.TemporaryDirectory()`.

### Fixture-style test data

Many tests copy fixture docs with `shutil.copytree(...)` from nearby `docs/` folders.

### Mocked change detection

Cascade tests patch change input (for example `_get_changed_files`) to avoid relying on real git history.

## CI-Relevant Commands

Local equivalents of CI jobs:

```bash
make check          # ruff check + ruff format --check
make test           # pytest -v
make practical-test # docsync check docs/
```

---

related docs:
- docs/repo/tooling.md - pytest configuration
- docs/repo/cicd.md    - CI test jobs

related sources:
- tests/cascade/ - cascade tests
- tests/parser/  - parser tests
- tests/tree/    - tree tests
- tests/check/   - validation tests
- tests/config/  - config tests
- tests/prompt/  - prompt tests
