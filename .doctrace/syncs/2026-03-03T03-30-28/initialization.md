# Sync Report: docs/features/initialization.md

## Status: UNCHANGED

No factual errors found. The document remains accurate against the current source code.

## Checked Sources

| Source | Status |
|--------|--------|
| src/doctrace/commands/init.py | valid, content matches doc |
| src/doctrace/core/config.py | valid, init_config function unchanged |
| src/doctrace/core/constants.py | valid, defaults match doc |

## Checked References

| Reference | Status |
|-----------|--------|
| docs/overview.md (related_doc) | valid, file exists |

## Triggered By

- `src/doctrace/core/config.py` changed (removed Base class, added ignore_inline_refs)
- `src/doctrace/commands/info.py` changed (added ignore pattern support)

## Analysis

The changes that triggered this review do not affect the initialization doc:

1. **Removed Base class / save_config / update_base** - The init command never used these. `init_config()` is unchanged.
2. **Added `ignore_inline_refs` config field** - This is a new config option used by the `info` command. The init doc describes what `doctrace init` creates (an empty `{}` config) and shows optional metadata customization. It does not claim to be a full config reference, so not documenting `ignore_inline_refs` here is not a factual error.
3. **Deleted doctrace.json from repo root** - This was the project's own config file, not related to the doc's description of what `doctrace init` creates.

## Notes

- The doc says the config is created "at repo root" but the code uses `Path.cwd()`. In practice these are the same since users run the command from repo root, and the doc is not misleading.
- The output example shows `Created doctrace.json` but the actual output includes the full path. This is a simplification in the doc, not a factual error.
