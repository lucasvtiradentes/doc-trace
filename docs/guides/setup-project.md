---
title: Setup Project
description: Guide to setting up doctrace development environment
related_docs:
  - docs/repo/local-setup.md: quick reference
sources:
  - Makefile: make command definitions
  - pyproject.toml: dependency definitions
---

Guide to setting up doctrace development environment.

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
.venv/bin/doctrace --version
```

Should output the installed package version, e.g. `doctrace 0.1.1`

## Running Commands

### With Activated Venv

```bash
source .venv/bin/activate
doctrace info docs/
doctrace affected docs/ --last 1
doctrace preview docs/
```

### Without Activation

```bash
.venv/bin/doctrace info docs/
.venv/bin/doctrace affected docs/ --last 1
.venv/bin/doctrace preview docs/
```

## Available Make Commands

| Command              | Description                  |
|----------------------|------------------------------|
| make install         | setup venv + deps            |
| make check           | lint + format check          |
| make test            | run pytest                   |
| make practical-test  | run doctrace info docs/   |
| make changelog       | build CHANGELOG.md           |
| make changelog-draft | preview changelog            |

## Initialize Doctrace in Your Project

After installation:

```bash
doctrace init
```

Creates `doctrace.json` with default config.

