## Confidence
high

## Files read
- src/docsync/commands/preview/__init__.py - exports run() from server module
- src/docsync/commands/preview/server.py - HTTP server with PreviewHandler, run() entry point, endpoints for /, /doc, /history, /search
- src/docsync/commands/preview/graph.py - build_graph_data() and generate_html(), uses tree.py for dependency data
- src/docsync/commands/preview/tree.py - build_dependency_tree(), DependencyTree namedtuple, level computation
- src/docsync/commands/preview/search.py - search_docs() for full-text search across markdown files
- src/docsync/commands/preview/template.html - SPA with mermaid graph, markdown editor, tree/level navigation, search
- src/docsync/core/git.py - get_file_history() and get_file_at_commit() used by server.py
- docs/concepts.md - related doc, core types still valid
- docs/architecture.md - references preview command, confirms module structure

## Metadata updates
- Added source: src/docsync/core/git.py (server.py imports get_file_history and get_file_at_commit from this module)

## Changes made
- Restructured Implementation table: added Module column to clarify which file each function lives in
- Added run() to Implementation table (entry point in server.py, was missing)
- Added build_dependency_tree() to Implementation table (key function in tree.py, was missing)
- Removed get_file_history() and get_file_at_commit() from Implementation table (these live in core/git.py, not the preview module; tracked via related sources instead)
- Added src/docsync/core/git.py to related sources metadata

## Why it was wrong
- The Implementation table was missing run() (server.py:113) and build_dependency_tree() (tree.py:17), two key functions in the preview module. run() is the actual entry point dispatched from cli.py, and build_dependency_tree() computes the dependency levels and circular refs that feed the graph visualization.
- get_file_history() and get_file_at_commit() were listed in the Implementation table as if they were part of the preview module, but they live in src/docsync/core/git.py. Adding git.py as a related source is more accurate than listing external functions as preview implementations.
- The related sources metadata only listed the preview directory, missing the dependency on core/git.py which server.py directly imports.
