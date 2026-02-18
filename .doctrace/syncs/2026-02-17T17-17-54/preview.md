## Confidence
high

## Files read
- src/docsync/commands/preview/__init__.py - exports run from server module
- src/docsync/commands/preview/graph.py - build_graph_data() and generate_html() functions, builds nodes/edges/levels from dependency tree
- src/docsync/commands/preview/search.py - search_docs() function, case-insensitive content search with max 3 matches per file
- src/docsync/commands/preview/server.py - PreviewHandler with GET/POST endpoints (/, /doc, /history, /search), run() function with default port 8420, auto browser open
- src/docsync/commands/preview/tree.py - build_dependency_tree() returns DependencyTree(levels, circular, doc_deps)
- src/docsync/commands/preview/template.html - full SPA with mermaid graph, folder tree, level list, search, doc viewer/editor, git history panel, SVG export, keyboard shortcuts (ArrowLeft/Right for main view, t/l for sidebar view)
- src/docsync/core/git.py - get_file_history() and get_file_at_commit() used by server
- docs/concepts.md - related doc, core types referenced

## Changes made
No changes needed

## Why it was wrong
The documentation accurately reflects the current source code. All features (dependency graph with SVG export, document viewer/editor, git history with version comparison, full-text search, keyboard shortcuts, bidirectional sidebar-graph selection sync), server endpoints (/, /doc GET/POST, /history, /search), configuration (--port with default 8420), implementation functions (build_graph_data, generate_html, PreviewHandler, get_file_history, get_file_at_commit, search_docs), and output messages match the implementation.
