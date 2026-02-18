# Update Documentation (Legacy)

Read ALL source files in this repository and update documentation accordingly.

## Instructions

1. Read ALL files from these folders (in parallel):
   - `src/doctrace/` - Python CLI source code
   - `.github/` - Workflows and scripts
   - `tests/` - Test files

2. Also read root files:
   - `README.md`
   - `CLAUDE.md`
   - `pyproject.toml`

3. Read ALL docs in `docs/` folder

4. Compare docs vs code field-by-field, update outdated sections

## Folders to Skip

- `.git/`, `.claude/`, `.ignore/`, `.venv/`, `__pycache__/`
- `.doctrace/syncs/` - sync output files
- `.pytest_cache/`
- Binary files (images, videos)

## What to Update

- File structure diagrams (must match actual folders/files)
- CLI commands and flags
- Configuration options
- Function names and entry points
- New features or removed features

## How to Compare (CRITICAL)

Do NOT just eyeball docs and conclude "looks correct". For each doc file:

1. Identify every table, list, or reference to source code
2. Open the referenced source file
3. Compare EACH field/value/function name against the actual code
4. Check for missing items (new commands, new flags, new options not in docs)
5. Check for removed items (commands/options that no longer exist in code)

Examples of things to verify field-by-field:
- CLI commands table → compare against `src/doctrace/cli.py` and `src/doctrace/commands/`
- Config options → compare against `src/doctrace/core/config.py`
- Metadata format → compare against `src/doctrace/core/parser.py`
- Lock file format → compare against `src/doctrace/core/lock.py`
- Git operations → compare against `src/doctrace/core/git.py`
- Validation rules → compare against `src/doctrace/commands/validate.py`
- Affected algorithm → compare against `src/doctrace/commands/affected.py`
- Preview features → compare against `src/doctrace/commands/preview/`

## Style Rules

- Keep docs concise, no fluff
- Tables must be aligned (equal column spacing)
- ASCII diagrams must have consistent box widths
- Use existing format as reference
- No emojis unless already present
- English only

## Table Format Example

```md
| Column One | Column Two | Column Three |
|------------|------------|--------------|
| value      | value      | value        |
| longer val | short      | medium value |
```

## Files to Check

- docs/overview.md
- docs/architecture.md
- docs/concepts.md
- docs/rules.md
- docs/testing.md
- docs/features/*.md
- docs/guides/*.md
- docs/repo/*.md

## Output

After updates, list what changed in each file.
