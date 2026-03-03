# Sync Report: docs/features/preview.md

## Status: UP TO DATE

No changes needed.

## Checked Sources

- `src/doctrace/commands/preview/graph.py` - verified
- `src/doctrace/commands/preview/template.html` - verified
- `src/doctrace/commands/preview/server.py` - verified
- `src/doctrace/commands/preview/search.py` - verified
- `src/doctrace/core/git.py` - verified

## Related Docs

- `docs/concepts.md` - verified, no impact

## Relevant Changes

- `c68c970 refactor(preview): rename Independent to Level 0` renamed "Independent" to "Level 0" in `graph.py` (label generation and `stats.independent` -> `stats.level_0`) and `template.html` (two label assignments). This doc was not affected because it never referenced the term "Independent" -- line 45 uses the generic phrase "Level-based grouping view" which remains accurate.

## Verification Details

| Section | Status | Notes |
|---------|--------|-------|
| Usage examples | ok | `--port` flag confirmed in `run()` signature |
| Features list | ok | All features confirmed in template.html and server.py |
| Navigation list | ok | "Level-based grouping view" is generic, unaffected by rename |
| Server Endpoints table | ok | All 5 endpoints match server.py |
| Configuration (--port default 8420) | ok | Uses `DEFAULT_PREVIEW_PORT` from constants |
| Implementation table | ok | All 6 functions/classes confirmed in source |
| Output section | ok | Matches server.py print statements |
| Frontmatter sources | ok | Paths are valid |
