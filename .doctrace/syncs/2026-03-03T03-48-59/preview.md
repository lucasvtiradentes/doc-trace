# Sync Report: docs/features/preview.md

## Trigger

Changed files since docs-base:
- `src/doctrace/commands/preview/graph.py` (M)
- `src/doctrace/commands/preview/template.html` (M)

Relevant commit: `c68c970 refactor(preview): rename Independent to Level 0`

## Sources Reviewed

- `src/doctrace/commands/preview/__init__.py`
- `src/doctrace/commands/preview/graph.py`
- `src/doctrace/commands/preview/server.py`
- `src/doctrace/commands/preview/search.py`
- `src/doctrace/commands/preview/template.html`
- `src/doctrace/core/git.py`
- `src/doctrace/core/constants.py`

## Related Docs Reviewed

- `docs/concepts.md`

## Changes Made

### 1. Removed "created date" from doc stats list (line 40)

- **Before:** `Doc stats (versions, updated date, created date, line count)`
- **After:** `Doc stats (versions, updated date, line count)`
- **Reason:** The `createdAt` variable is computed in `template.html` (line 409) but is never rendered in the UI. The breadcrumb stats only display `versions`, `updated` date, and `lineCount` (lines 428-430). Listing "created date" as a visible stat is factually incorrect.

## No Change Needed

### Rename from "Independent" to "Level 0"

The commit `c68c970` renamed the level-0 label from "Independent" to "Level 0" in both `graph.py` and `template.html`. However, the doc never used the term "Independent" -- it says "Level-based grouping view" which remains accurate. No change required.

## Verified (Accurate)

- Mermaid-based dependency diagram: confirmed (template.html uses mermaid@11)
- Nodes colored by dependency level: confirmed (levelColors array)
- Click to highlight node: confirmed (click handler calls highlightNode)
- Double-click to open doc in editor: confirmed (dblclick handler)
- Export graph as SVG: confirmed (exportSVG function)
- Markdown rendering via marked.js: confirmed (marked@15)
- Edit docs directly in browser: confirmed (POST /doc endpoint)
- View git history: confirmed (/history endpoint, get_file_history)
- Compare versions with diff highlighting: confirmed (computeDiff, generateDiffSummary)
- Folder tree view (collapsible): confirmed (tree view in sidebar)
- Level-based grouping view: confirmed (buildLevelList function)
- Full-text search: confirmed (search_docs, /search endpoint)
- Bidirectional selection sync: confirmed (selectDoc updates sidebar and graph)
- Keyboard shortcuts (left/right, t/l): confirmed (keyboardShortcuts object)
- All five server endpoints (/, /doc GET, /doc POST, /history, /search): confirmed
- Default port 8420: confirmed (DEFAULT_PREVIEW_PORT constant)
- All implementation table functions: confirmed (build_graph_data, generate_html, PreviewHandler, get_file_history, get_file_at_commit, search_docs)
- Output message and auto-open browser: confirmed (server.py lines 142-144)
