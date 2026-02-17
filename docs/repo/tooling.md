# Tooling

## Linting and Formatting

### Ruff

Fast Python linter and formatter.

| Setting     | Value           |
|-------------|-----------------|
| Line length | 120             |
| Rules       | E, F, I         |

Rules enabled:
- E - pycodestyle errors
- F - pyflakes
- I - isort (import sorting)

```bash
ruff check .        # lint
ruff format .       # format
ruff format --check # check formatting
```

## Testing

### Pytest

Test framework configured via `pyproject.toml`.

| Setting     | Value             |
|-------------|-------------------|
| testpaths   | tests/            |
| python_files| test.py, test_*.py|

```bash
pytest -v           # run tests verbose
```

## Build

### Hatch

Build backend for wheel packaging.

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/docsync"]
```

## Changelog

### Towncrier

Changelog generation from fragments.

| Setting        | Value                          |
|----------------|--------------------------------|
| directory      | .changelog                     |
| filename       | CHANGELOG.md                   |
| title_format   | ## {version} ({project_date})  |

Fragment types:
- `feature/` - new features
- `bugfix/`  - bug fixes
- `misc/`    - other changes

```bash
towncrier build --yes --version X.Y.Z
towncrier build --draft --version X.Y.Z  # preview
```

## Versioning

### Bump2version

Version bumping tool included in `dev` optional dependencies.

```bash
bump2version patch  # 0.1.0 → 0.1.1
bump2version minor  # 0.1.0 → 0.2.0
bump2version major  # 0.1.0 → 1.0.0
```

---

related docs:
- docs/repo/local-setup.md - using these tools locally
- docs/repo/cicd.md        - tools in CI pipelines

related sources:
- pyproject.toml - tool configurations
- Makefile       - tool commands
