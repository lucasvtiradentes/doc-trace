# Sync Report: docs/rules.md

## Flagged Sources

- `src/doctrace/core/config.py` (changed: removed Base class; added ignore_inline_refs config key; changed valid_keys)

## Findings

### No direct impact from flagged changes

The doc does not reference the `base` config key, `--since-base` flag, or Base class that were removed. The doc does not list config keys, so the addition of `ignore_inline_refs` does not require a doc update here. This is a coding rules/conventions doc, not a config reference doc.

### Factual errors found (pre-existing, unrelated to flagged changes)

1. **Line 55 (Lowercase CLI section)**: Listed `validate` and `lock` as commands. Neither exists in the codebase. The actual commands are `info`, `affected`, `preview`, `init`, `index`, `completion` (per `cli.py` and `src/doctrace/commands/`).
   - **Fixed**: Replaced command list with the correct set of commands.

2. **Line 77 (Exhaustive Dependency Crawling section)**: Referenced `affected_depth_limit` as a mechanism to limit recursion. No such config key, parameter, or variable exists anywhere in the source code. The `_propagate()` function in `affected.py` has no depth limit parameter.
   - **Fixed**: Removed the reference to the non-existent `affected_depth_limit` while keeping the anti-pattern guidance.

### Items reviewed but not changed

- **Single-Responsibility Commands (lines 16-20)**: Lists 4 commands (info, affected, preview, init) but the codebase has 6 (also index, completion). The section says "Each command does one thing" and the listed commands are accurate; the list is not claimed to be exhaustive. Not changed.
- **Lazy Error Recovery (line 38)**: References `validate` as a concept rather than a command name. In context ("On parse errors in `validate`") this reads as referring to the validation phase of the info command, which is accurate behavior. Not changed.
- **NamedTuple for Results (lines 63-67)**: Lists RefEntry, ParsedDoc, AffectedResult, DependencyTree. All four are indeed NamedTuples in the source. Note: ValidateResult and RefError (in info.py) are dataclasses, not NamedTuples, but the doc does not list those. Accurate as-is.
- **Frontmatter**: Sources and related_docs all resolve correctly. No changes needed.

## Changes Applied

| Line | Before | After | Reason |
|------|--------|-------|--------|
| 55 | `validate`, `affected`, `preview`, `lock`, `init` | `info`, `affected`, `preview`, `init`, `index`, `completion` | `validate` and `lock` do not exist as commands |
| 77 | Do not recursively follow all refs without limits. Use `affected_depth_limit`. | Do not recursively follow all refs without limits. | `affected_depth_limit` does not exist in the codebase |
