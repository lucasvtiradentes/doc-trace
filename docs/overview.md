# Docsync Overview

CLI tool that keeps documentation in sync with code changes.

## What It Does

- Detects docs affected by code changes via git diff
- Validates all doc references point to existing files
- Generates AI prompts for doc review with dependency ordering
- Tracks doc-to-doc relationships for cascading updates

## Package Info

| Field       | Value                       |
|-------------|:----------------------------|
| Name        | docsync                     |
| Version     | 0.1.0                       |
| Python      | 3.9+                        |
| Entry point | docsync.cli:main            |
| Build       | hatch (wheel packaging)     |

## Built With

- argparse   - CLI argument parsing
- pathlib    - path handling
- subprocess - git operations
- fnmatch    - pattern matching for ignored paths
- json       - config/lock file handling

## Commands

| Command | Description                          |
|---------|:-------------------------------------|
| check   | validate all doc refs exist          |
| cascade | list docs affected by git diff       |
| prompt  | generate AI prompt for doc review    |
| tree    | show doc dependency graph            |
| init    | create .docsync/ config directory    |

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
| docs/features/validation.md      | check command reference validation       |
| docs/features/cascade.md         | cascade command change detection         |
| docs/features/prompt-generation.md | prompt command AI task generation      |
| docs/features/dependency-tree.md | tree command dependency visualization    |
| docs/features/initialization.md  | init command project setup               |
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
