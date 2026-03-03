# Sync Report: docs/features/index-cmd.md

## Sources Checked
- src/doctrace/commands/index.py
- src/doctrace/core/docs.py
- src/doctrace/cli.py (CLI argument definitions)

## Related/Required Docs Checked
- docs/concepts.md
- docs/features/validation.md

## Changes Made

### 1. Fixed sort description (line 25)
- **Before:** `Generates a markdown table sorted by filename`
- **After:** `Generates a markdown table sorted by category, then filename`
- **Reason:** `_build_rows` sorts by `(sort_cat, str(rel_path).lower())`, which is category first, then filename. The doc omitted the category sort.

### 2. Fixed output format example (lines 29-36)
- **Before:** Table heading was `## Doc Index` with only `File` and `Description` columns.
- **After:** Table heading is `## Documentation Index` with `Category`, `File`, `Description`, `Rel. docs`, `Req. docs`, `Sources` columns.
- **Reason:** `INDEX_MARKER` in source is `"## Documentation Index"`, not `"## Doc Index"`. `_render_table` produces a 6-column table including Category, Rel. docs, Req. docs, and Sources columns which were missing from the example.

### 3. Fixed function name in Implementation section (line 54)
- **Before:** `Uses get_docs_metadata() to extract frontmatter`
- **After:** `Uses build_doc_index() to extract frontmatter`
- **Reason:** `get_docs_metadata()` does not exist anywhere in the codebase. The actual function called in `index.run()` is `build_doc_index()` from `src/doctrace/core/docs.py`.

## Notes

- The frontmatter `related_docs` entry references `docs/concepts.md` with description "DocMeta type". There is no type named `DocMeta` in that file or the codebase; the relevant types are `ParsedDoc` and `DocIndex`. This is a minor inaccuracy in a description field and the path itself is valid, so no change was made.
- Frontmatter `sources` entries are accurate and point to existing files.
- Usage example, Options table, and Frontmatter Fields Used table are all accurate per the CLI definition and source code.
