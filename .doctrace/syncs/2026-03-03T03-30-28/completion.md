# Sync Report: docs/features/completion.md

## Status: UP TO DATE

No changes needed.

## Sources Checked

| Source | Status |
|---|---|
| `src/doctrace/commands/completion.py` | verified |
| `src/doctrace/cmd_registry.py` | verified |

## Related Docs Checked

| Doc | Status |
|---|---|
| `docs/overview.md` | consistent |

## Findings

The doc was flagged because `src/doctrace/cli.py` and `src/doctrace/cmd_registry.py` changed (removal of `base` command, `--since-base`/`--verbose` flags; addition of `--ignore` flag). However, the doc already reflects the current state of the code:

- The "What Gets Completed" table lists `--json --ignore` for `info`, which matches `cmd_registry.py` line 17.
- The "What Gets Completed" table lists `--last --base-branch --since --json --ignore` for `affected`, which matches `cmd_registry.py` line 23.
- The `index` flags (`-o --output`), `completion` subcommands (`zsh bash fish`), and `info <TAB>` (directories) are all accurate.
- No references to removed commands (`base`) or removed flags (`--since-base`, `--verbose`, `-V`) exist in this doc.

The doc was likely already updated in commit `109efb7` ("docs: remove --verbose references, add --ignore to completion").

## Changes Applied

None.
