# Local Setup

## Requirements

- Python 3.9+
- make (optional, for convenience commands)

## Install

```bash
make install
```

This creates `.venv/` and installs package with dev dependencies.

## Dev Dependencies

| Package      | Purpose                    |
|--------------|----------------------------|
| pytest       | testing framework          |
| ruff         | linter and formatter       |
| towncrier    | changelog generation       |
| bump2version | version bumping            |

## Available Commands

| Command              | Description                       |
|----------------------|-----------------------------------|
| make install         | create venv, install deps         |
| make check           | ruff lint + format check          |
| make test            | pytest -v                         |
| make practical-test  | doctrack validate docs/            |
| make changelog       | build CHANGELOG.md                |
| make changelog-draft | preview changelog                 |

## Manual Install

If not using make:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Running Commands

After install, use the venv:

```bash
.venv/bin/doctrack validate docs/
.venv/bin/doctrack affected docs/ --last 1
.venv/bin/doctrack preview docs/
.venv/bin/doctrack init
```

Or activate the venv:

```bash
source .venv/bin/activate
doctrack validate docs/
```

---

related docs:
- docs/repo/tooling.md - tool configurations

related sources:
- Makefile       - command definitions
- pyproject.toml - project dependencies
