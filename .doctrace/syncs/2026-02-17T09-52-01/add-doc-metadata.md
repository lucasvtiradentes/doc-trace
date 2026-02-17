## Changes made
- Updated guide to distinguish default `custom` style vs optional `frontmatter` style.
- Clarified separator behavior (`require_separator`) and that custom style requires `- path - description`.
- Adjusted wording around directory/glob refs to parser-level behavior.

## Why it was wrong
- `src/docsync/core/parser.py` supports both custom and frontmatter parsing with different list-item patterns.
- `src/docsync/core/parser.py::_get_custom_section` behavior depends on `require_separator`; separator is not universally mandatory.
- `src/docsync/core/parser.py::_extract_section` uses `LIST_ITEM` for custom style (description required) and `LIST_ITEM_SIMPLE` for frontmatter (description optional).
