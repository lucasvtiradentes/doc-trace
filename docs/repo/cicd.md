# CI/CD

## Pipelines

| Workflow         | Trigger              | Purpose                  |
|------------------|----------------------|--------------------------|
| prs.yml          | pull_request         | validate PRs             |
| push-to-main.yml | push to main         | validate main branch     |
| callable-ci.yml  | workflow_call        | reusable CI workflow     |
| release.yml      | workflow_dispatch    | publish to PyPI          |

## CI Jobs (callable-ci.yml)

### check

Runs linting and format checking.

```yaml
steps:
  - pip install -e ".[dev]"
  - ruff check .
  - ruff format --check .
```

### test

Runs pytest with Python version matrix.

| Python | Status     |
|--------|------------|
| 3.9    | tested     |
| 3.12   | tested     |

```yaml
steps:
  - pip install -e ".[dev]"
  - pytest -v
```

### practical-test

Runs docsync against its own docs.

```yaml
steps:
  - pip install -e ".[dev]"
  - docsync validate docs/
```

## Release Pipeline

Triggered manually via workflow_dispatch with version bump type selection.

Steps:
1. Checkout with full history
2. Setup Python 3.12
3. Install bump2version, towncrier, hatch
4. Bump version (if not initial)
5. Build changelog
6. Commit and tag
7. Push to main with tags
8. Build wheel
9. Publish to PyPI

### PyPI Publishing

Uses `pypa/gh-action-pypi-publish` with trusted publisher (OIDC).

Environment: `pypi`

### Version Bump Options

| Option  | Example         |
|---------|-----------------|
| patch   | 0.1.0 → 0.1.1   |
| minor   | 0.1.0 → 0.2.0   |
| major   | 0.1.0 → 1.0.0   |
| initial | no bump         |

## Branch Strategy

- `main` - primary branch for push workflow
- Tagged releases: `v0.1.0`, `v0.2.0`, etc.

---

related docs:
- docs/repo/tooling.md     - tool configurations
- docs/repo/local-setup.md - local equivalents

related sources:
- .github/workflows/prs.yml          - PR workflow
- .github/workflows/push-to-main.yml - main branch workflow
- .github/workflows/callable-ci.yml  - reusable CI
- .github/workflows/release.yml      - release workflow
