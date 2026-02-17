## Changes made
- Corrected parse-error guidance to reflect non-zero exit behavior in `check`.
- Removed misleading lock-file guidance and aligned with actual lock usage/location.
- Updated anti-pattern wording to emphasize accumulate-and-fail behavior.

## Why it was wrong
- `src/docsync/commands/check.py` continues scanning after parse errors but returns exit code 1 when any errors are present.
- `src/docsync/core/lock.py` stores lock state in `.docsync/lock.json`; ignore behavior is only explicitly added for `.docsync/syncs/` in `config.py`.
