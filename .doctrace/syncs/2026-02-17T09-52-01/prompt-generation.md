## Changes made
- Corrected `--incremental` description to affected-doc behavior (direct + cascade), not just changed docs.
- Updated lock example to include `last_run` and `docs_validated`.
- Clarified sync directory timestamp format.

## Why it was wrong
- `src/docsync/commands/prompt.py::generate_validation_report` filters by `find_affected_docs(...)` results when lock commit exists.
- `src/docsync/core/lock.py::save_lock` sets `last_run`, and `Lock.to_dict()` includes `docs_validated`.
- `src/docsync/commands/prompt.py::_get_syncs_dir` uses `%Y-%m-%dT%H-%M-%S`.
