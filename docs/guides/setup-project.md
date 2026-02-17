# Setup Project

Guide to setting up docsync development environment.

## Requirements

- Python 3.9 or higher
- make (optional, for convenience commands)

## Quick Setup

```bash
make install
```

This creates a virtual environment and installs all dependencies.

## Manual Setup

If make is not available:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Dev Dependencies

Installed with `.[dev]`:

| Package      | Version | Purpose              |
|--------------|---------|----------------------|
| pytest       | >= 7    | test framework       |
| ruff         | >= 0.9  | linter/formatter     |
| towncrier    | >= 23   | changelog generation |
| bump2version | >= 1    | version bumping      |

## Verify Installation

```bash
.venv/bin/docsync --version
```

Should output: `docsync 0.1.0`

## Running Commands

### With Activated Venv

```bash
source .venv/bin/activate
docsync validate docs/
docsync affected docs/ --last 1
docsync tree docs/
docsync preview docs/
```

### Without Activation

```bash
.venv/bin/docsync validate docs/
.venv/bin/docsync affected docs/ --last 1
.venv/bin/docsync tree docs/
.venv/bin/docsync preview docs/
```

## Available Make Commands

| Command              | Description                  |
|----------------------|------------------------------|
| make install         | setup venv + deps            |
| make check           | lint + format check          |
| make test            | run pytest                   |
| make practical-test  | run docsync validate docs/   |
| make changelog       | build CHANGELOG.md           |
| make changelog-draft | preview changelog            |

## Initialize Docsync in Your Project

After installation:

```bash
docsync init
```

Creates `.docsync/` with default config.

---

related docs:
- docs/repo/local-setup.md - quick reference

related sources:
- Makefile       - make command definitions
- pyproject.toml - dependency definitions
