## Confidence
high

## Files read
- docs/features/preview.md - the doc being validated
- src/docsync/commands/preview/__init__.py - module entry, re-exports run()
- src/docsync/commands/preview/server.py - PreviewHandler, run(), endpoint logic
- src/docsync/commands/preview/graph.py - build_graph_data(), generate_html()
- src/docsync/commands/preview/search.py - search_docs() implementation
- src/docsync/commands/preview/tree.py - DependencyTree, build_dependency_tree()
- src/docsync/commands/preview/template.html - full SPA: mermaid graph, marked.js rendering, keyboard shortcuts, SVG export, bidirectional sync, diff highlighting
- src/docsync/core/git.py - get_file_history(), get_file_at_commit() used by server.py
- docs/concepts.md - related doc, core types
- docs/architecture.md - checked for related doc relevance

## Metadata updates
- Added source: src/docsync/core/git.py (server.py imports get_file_history and get_file_at_commit from it)

## Changes made
- Changed "Markdown rendering with syntax highlighting" to "Markdown rendering via marked.js" (no syntax highlighting library is loaded, only marked.js for markdown parsing)
- Added "Bidirectional selection sync between sidebar and graph" to Navigation features (feature from commit b172f98 was missing)
- Changed "Keyboard shortcuts (arrow keys, t/l for views)" to "Keyboard shortcuts (left/right arrows for views, t/l for sidebar)" (only left/right arrows are bound, not all arrow keys; clarified t/l control sidebar not main views)
- Added src/docsync/core/git.py to related sources metadata

## Why it was wrong
- "syntax highlighting" was inaccurate: template.html only loads marked.js for markdown rendering, no highlight.js or prism.js is included. The word "highlighting" in the codebase refers to diff highlighting (showing changes between versions), not code syntax highlighting.
- Bidirectional selection sync (commit b172f98) was a new feature not reflected in the doc. The highlightNode() function accepts a fromSidebar parameter, and selectDoc() updates both sidebar selection and graph highlight.
- "arrow keys" was misleading: keyboardShortcuts object in template.html only binds ArrowLeft (diagram) and ArrowRight (editor), not ArrowUp/ArrowDown. Also t/l switch the sidebar view (tree/levels), not the main view.
- src/docsync/core/git.py was missing from sources despite server.py importing get_file_history and get_file_at_commit directly from it.
