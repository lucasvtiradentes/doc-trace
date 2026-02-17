## Confidence
high

## Files read
- docs/architecture.md - Architecture diagrams/flows and metadata.
- docs/concepts.md - Related type definitions.
- docs/features/affected.md - Affected algorithm details referenced by architecture doc.
- docs/features/validation.md - Validate flow details referenced by architecture doc.
- docs/features/preview.md - Preview module structure references.
- src/docsync/cli.py - Command dispatch and module usage.
- src/docsync/commands/affected.py - `AffectedResult` field names.
- src/docsync/commands/preview/__init__.py - Preview command module now package-based.
- src/docsync/commands/preview/server.py - Preview runtime entrypoint.
- src/docsync/commands/validate.py - Validation flow behavior.
- src/docsync/core/ - Shared modules and responsibilities.

## Metadata updates
No metadata changes.

## Changes made
- Updated entry-point diagram path from `commands/preview.py` to `commands/preview/`.
- Updated `AffectedResult` field summary to `affected_docs, direct_hits, indirect_hits, circular_refs, matches, indirect_chains`.

## Why it was wrong
The implementation now dispatches preview via the `preview/` package and `AffectedResult` uses explicit field names from `src/docsync/commands/affected.py`; the previous text used outdated labels.
