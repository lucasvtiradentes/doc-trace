# Docsync Overview

CLI tool that keeps documentation in sync with code changes.

## What It Does

- Detects docs affected by code changes via git diff
- Validates all doc references point to existing files
- Tracks doc-to-doc relationships for cascading updates
- Manages lock state for incremental analysis

## Package Info

| Field       | Value                       |
|-------------|:----------------------------|
| Name        | docsync                     |
| Version     | 0.1.2                       |
| Python      | 3.9+                        |
| Entry point | docsync.cli:main            |
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
| validate | validate all doc refs exist          |
| affected | list docs affected by git diff       |
| preview  | interactive docs explorer in browser |
| lock     | manage lock.json state               |
| init     | create .docsync/ config directory    |

## Doc Index

| File                             | Description                              |
|----------------------------------|------------------------------------------|
| docs/overview.md                 | project summary and doc index            |
| docs/architecture.md             | system design, data flow, diagrams       |
| docs/concepts.md                 | key types and terminology                |
| docs/repo/structure.md           | directory layout and file organization   |
| docs/repo/tooling.md             | dev tools and configurations             |
| docs/repo/local-setup.md         | local development setup                  |
| docs/repo/cicd.md                | CI/CD pipelines and deployment           |
| docs/features/validation.md      | validate command reference validation    |
| docs/features/affected.md        | affected command change detection        |
| docs/features/initialization.md  | init command project setup               |
| docs/features/preview.md         | preview command interactive explorer     |
| docs/rules.md                    | coding principles and conventions        |
| docs/testing.md                  | testing strategy and patterns            |
| docs/guides/setup-project.md     | how to set up dev environment            |
| docs/guides/add-doc-metadata.md  | how to add metadata to docs              |
| docs/guides/validate-docs.md     | how to validate doc references           |

---

related docs:
- docs/architecture.md - system design details
- docs/concepts.md     - key terminology

related sources:
- src/docsync/cli.py - main entry point
- src/docsync/       - main package directory
