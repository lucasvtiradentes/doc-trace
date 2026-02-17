# Preview (preview command)

Interactive documentation explorer in the browser.

## Usage

```bash
docsync preview docs/
docsync preview docs/ --port 8080
```

## What It Does

Starts a local HTTP server serving an interactive single-page application for exploring documentation.

## Features

### Dependency Graph Visualization

- Interactive mermaid-based dependency diagram
- Nodes colored by dependency level
- Click to highlight node and its connections
- Double-click to open doc in editor
- Export graph as SVG

### Document Viewer/Editor

- Markdown rendering with syntax highlighting
- Edit docs directly in browser
- View git history for each doc
- Compare versions with diff highlighting
- Doc stats (versions, updated date, created date, line count)

### Navigation

- Folder tree view (collapsible)
- Level-based grouping view
- Full-text search across all docs
- Keyboard shortcuts (arrow keys, t/l for views)

## Server Endpoints

| Endpoint | Method | Description                          |
|----------|--------|--------------------------------------|
| /        | GET    | main HTML application                |
| /doc     | GET    | fetch doc content (supports ?commit=)|
| /doc     | POST   | save doc content                     |
| /history | GET    | get git commit history for doc       |
| /search  | GET    | search docs by content               |

## Configuration

### --port

Change the server port (default: 8420).

```bash
docsync preview docs/ --port 3000
```

## Implementation

| Function            | Purpose                                  |
|---------------------|------------------------------------------|
| build_graph_data()  | build nodes/edges from dependency tree   |
| generate_html()     | inject graph data into template          |
| PreviewHandler      | HTTP request handler                     |
| get_file_history()  | git log for file                         |
| get_file_at_commit()| git show for file at commit              |
| search_docs()       | content search across docs               |

## Output

```
Serving docs preview at http://localhost:8420
Press Ctrl+C to stop
```

Opens browser automatically.

---

related docs:
- docs/concepts.md - core types

related sources:
- src/docsync/commands/preview/ - preview module
