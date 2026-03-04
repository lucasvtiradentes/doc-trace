---
title: Local Setup
description: Quick reference for local development setup
related_docs:
  - docs/repo/tooling.md: tool configurations
  - docs/index.md:        referenced in practical-test command
sources:
  - Makefile: command definitions
  - pyproject.toml: project dependencies
---

## Requirements

- Python 3.9+
- make (optional, for convenience commands)

## Install

```bash
make install
```

This creates `.venv/`, installs package with dev dependencies, and sets up pre-commit hooks.

## Dev Dependencies

| Package      | Purpose              |
|--------------|----------------------|
| pytest       | testing framework    |
| ruff         | linter and formatter |
| towncrier    | changelog generation |
| bump2version | version bumping      |
| pre-commit   | git hook management  |

## Available Commands

| Command              | Description                                 |
|----------------------|---------------------------------------------|
| make install         | create venv, install deps, setup pre-commit |
| make check           | ruff lint + format check                    |
| make test            | pytest -v                                   |
| make practical-test  | doctrace info docs/ --ignore docs/index.md  |
| make changelog       | build CHANGELOG.md                          |
| make changelog-draft | preview changelog                           |

## Manual Install

If not using make:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Running Commands

After install, use the venv:

```bash
.venv/bin/doctrace info docs/
.venv/bin/doctrace affected docs/ --last 1
.venv/bin/doctrace preview docs/
.venv/bin/doctrace init
```

Or activate the venv:

```bash
source .venv/bin/activate
doctrace info docs/
```

