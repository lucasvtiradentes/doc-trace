## Changes made
- Added `metadata` to `Config` fields.
- Softened circular-dependency wording to match command-specific handling.
- Corrected metadata-section definition to be config-driven, not always post-separator only.

## Why it was wrong
- `src/docsync/core/config.py::Config` includes `metadata: MetadataConfig`.
- Circular behavior differs between commands (`tree` vs `cascade` implementations).
- `src/docsync/core/parser.py` behavior depends on metadata style and `require_separator`.
