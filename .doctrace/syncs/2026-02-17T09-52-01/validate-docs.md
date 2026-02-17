## Changes made
- Fixed parse-error section to state parse failures are errors and contribute to non-zero exit.
- Simplified wildcard notes to align with implemented checks.

## Why it was wrong
- `src/docsync/commands/check.py::_check_single_doc` appends `RefError` on parse failure; `run()` returns 1 when any errors exist.
- Pattern behavior in this command path is implemented via `fnmatch.fnmatch` and `Path.glob` checks, not the previous detailed `**` claim.
