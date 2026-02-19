---
title: Overview
description: CLI tool that keeps documentation in sync with code changes
related_docs:
  - docs/architecture.md: system design details
  - docs/concepts.md: key terminology
sources:
  - src/doctrace/cli.py: main entry point
  - src/doctrace/: main package directory
---

CLI tool that keeps documentation in sync with code changes.

## What It Does

- Detects docs affected by code changes via git diff
- Validates all doc references point to existing files
- Tracks doc-to-doc relationships for cascading updates
- Manages base commit state for incremental analysis

## Package Info

| Field       | Value                       |
|-------------|:----------------------------|
| Name        | doctrace                     |
| Version     | 0.1.1                       |
| Python      | 3.9+                        |
| Entry point | doctrace.cli:main            |
| Build       | hatch (wheel packaging)     |

## Built With

- argparse   - CLI argument parsing
- pathlib    - path handling
- subprocess - git operations
- fnmatch    - pattern matching for ignored paths
- json       - config/lock/output handling

## Commands

| Command  | Description                          |
|----------|:-------------------------------------|
| info     | show phases + validate all doc refs  |
| affected | list docs affected by git diff       |
| preview  | interactive docs explorer in browser |
| base     | manage base commit state             |
| init     | create doctrace.json config file     |
