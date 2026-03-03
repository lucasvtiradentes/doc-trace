# Sync Report: docs/features/completion.md

## Sources Checked
- src/doctrace/commands/completion.py
- src/doctrace/cmd_registry.py
- src/doctrace/cli.py (supplementary)

## Related Docs Checked
- docs/overview.md

## Findings

No factual errors found. The documentation accurately reflects the source code.

### Details

- **Usage section**: The three shell variants (`zsh`, `bash`, `fish`) match `COMMANDS["completion"]["subcommands"]` in `cmd_registry.py` and the `generators` dict in `completion.py`.
- **Installation section**: The eval/source commands match the help text printed by `completion.run()` when no shell argument is given.
- **What Gets Completed table**: All six rows verified against `cmd_registry.py`:
  - `info` flags `--json --ignore` match registry.
  - `affected` flags `--last --base-branch --since --json --ignore` match registry.
  - `completion` subcommands `zsh bash fish` match registry.
  - `index` flags `-o --output` match registry.
  - Directory completion for `info` is correct (`info` is in `DIR_COMMANDS`).
  - All commands completing at `doctrace <TAB>` is correct.
- **Implementation section**: Accurately describes the role of `cmd_registry.py` as single source of truth for command metadata, which `completion.py` imports via `COMMANDS` and `DIR_COMMANDS`.
- **Frontmatter**: Sources and related_docs are all valid and correctly described.

## Changes Made
None. Documentation is accurate.
