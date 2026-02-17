# Repository Structure

```
doc-sync/
├── src/docsync/           ← main package
│   ├── __init__.py
│   ├── cli.py             ← entry point, argparse setup
│   ├── commands/          ← subcommand implementations
│   │   ├── __init__.py
│   │   ├── check.py       ← ref validation
│   │   ├── cascade.py     ← change detection
│   │   ├── prompt.py      ← AI prompt generation
│   │   ├── tree.py        ← dependency visualization
│   │   └── init.py        ← project initialization
│   ├── core/              ← shared logic
│   │   ├── __init__.py
│   │   ├── parser.py      ← metadata extraction
│   │   ├── config.py      ← config loading/validation
│   │   ├── lock.py        ← state persistence
│   │   └── constants.py   ← shared constants
│   └── prompts/
│       └── prompt.md      ← default prompt template
├── tests/                 ← pytest test suite
│   ├── __init__.py
│   ├── cascade/           ← cascade tests
│   ├── check/             ← validation tests
│   ├── config/            ← config validation tests
│   ├── parser/            ← parser tests
│   ├── prompt/            ← prompt generation tests
│   └── tree/              ← dependency tree tests
├── docs/                  ← documentation
├── .github/workflows/     ← CI/CD pipelines
│   ├── prs.yml            ← PR checks
│   ├── push-to-main.yml   ← main branch checks
│   ├── callable-ci.yml    ← reusable CI workflow
│   └── release.yml        ← PyPI release workflow
├── .changelog/            ← towncrier fragments
├── pyproject.toml         ← project config, deps
├── Makefile               ← dev commands
└── README.md
```

## Key Directories

### src/docsync/commands/

Each file implements one CLI subcommand. All follow the same pattern:
- Define command-specific types
- Implement core logic
- Export `run()` function called by cli.py

### src/docsync/core/

Shared modules used across commands:
- `parser.py`    - extracts metadata from markdown
- `config.py`    - loads and validates config.json
- `lock.py`      - manages lock.json state
- `constants.py` - file/dir names, default values

### tests/

Pytest tests grouped by feature area. Most tests use temporary directories and fixture docs copied from local test fixtures.

---

related docs:
- docs/repo/tooling.md - dev tools configuration
- docs/testing.md      - test patterns and coverage

related sources:
- src/docsync/       - main package
- tests/             - test suite
- .github/workflows/ - CI pipelines
