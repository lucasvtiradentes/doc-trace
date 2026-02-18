## Changes made
- Corrected behavior note for parse failures: they are reported as validation errors, not skipped silently.

## Why it was wrong
- `src/docsync/commands/check.py::_check_single_doc` emits `RefError` for parse exceptions, and `run()` exits non-zero if any result has errors.
