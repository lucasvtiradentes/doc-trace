## Changes made
- Removed incorrect `syncs/.gitignore` behavior and documented actual root `.gitignore` update.
- Updated idempotency notes to match append-if-missing behavior.

## Why it was wrong
- `src/docsync/core/config.py::init_docsync` creates `.docsync/` + `config.json` + `.docsync/syncs/`.
- `src/docsync/core/config.py::_add_syncs_to_gitignore` writes `.docsync/syncs/` to repository `.gitignore` and does not create `syncs/.gitignore`.
