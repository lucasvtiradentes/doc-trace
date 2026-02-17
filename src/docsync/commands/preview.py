from __future__ import annotations

import http.server
import json
import socketserver
import threading
import webbrowser
from pathlib import Path

from docsync.commands.tree import build_dependency_tree
from docsync.core.config import Config, find_repo_root, load_config


def build_graph_data(docs_path: Path, config: Config, repo_root: Path) -> dict:
    tree = build_dependency_tree(docs_path, config, repo_root)
    nodes = []
    edges = []
    node_ids: dict[Path, str] = {}
    doc_to_level: dict[Path, int] = {}
    for level_idx, level_docs in enumerate(tree.levels):
        for doc in level_docs:
            doc_to_level[doc] = level_idx
    for i, doc in enumerate(tree.doc_deps.keys()):
        node_id = f"N{i}"
        node_ids[doc] = node_id
        rel_path = str(doc.relative_to(repo_root))
        level = doc_to_level.get(doc, 0)
        nodes.append({
            "id": node_id,
            "path": rel_path,
            "name": doc.stem,
            "level": level,
        })
    for doc, deps in tree.doc_deps.items():
        for dep in deps:
            if dep in node_ids:
                edges.append({
                    "from": node_ids[dep],
                    "to": node_ids[doc],
                })
    for src, dst in tree.circular:
        if src in node_ids and dst in node_ids:
            edges.append({
                "from": node_ids[src],
                "to": node_ids[dst],
                "circular": True,
            })
    levels_info = []
    for i, level_docs in enumerate(tree.levels):
        levels_info.append({
            "level": i,
            "count": len(level_docs),
            "label": "Independent" if i == 0 else f"Level {i}",
        })
    return {
        "nodes": nodes,
        "edges": edges,
        "levels": levels_info,
        "stats": {
            "total": len(nodes),
            "independent": len(tree.levels[0]) if tree.levels else 0,
            "circular": len(tree.circular),
            "max_depth": len(tree.levels) - 1,
        },
    }


def generate_html(graph_data: dict) -> str:
    graph_json = json.dumps(graph_data)
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Docsync Preview</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #334155; }}
        .container {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 280px; background: #fff; padding: 20px; overflow-y: auto; border-right: 1px solid #e2e8f0; flex-shrink: 0; }}
        .main {{ flex: 1; display: flex; flex-direction: column; background: #f1f5f9; min-width: 0; }}
        .header {{ padding: 15px 20px; background: #fff; border-bottom: 1px solid #e2e8f0; }}
        .header-top {{ display: flex; align-items: center; justify-content: space-between; }}
        .header h1 {{ font-size: 18px; font-weight: 600; color: #1e293b; }}
        .tabs {{ display: flex; gap: 4px; }}
        .tab {{ padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; color: #64748b; transition: all 0.15s; }}
        .tab:hover {{ background: #f1f5f9; }}
        .tab.active {{ background: #3b82f6; color: white; }}
        .stats {{ margin-top: 8px; font-size: 13px; color: #64748b; }}
        .stats span {{ margin-right: 15px; }}
        .content {{ flex: 1; overflow: hidden; position: relative; }}
        .panel {{ position: absolute; inset: 0; padding: 20px; overflow: auto; transition: opacity 0.2s; }}
        .panel.hidden {{ opacity: 0; pointer-events: none; }}
        .graph-panel .mermaid {{ background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .graph-panel .mermaid svg {{ max-width: 100%; height: auto; }}
        .doc-panel {{ background: #fff; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 40px; max-width: 900px; margin: 0 auto; }}
        .doc-panel.empty {{ display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 14px; }}
        .doc-content {{ line-height: 1.7; }}
        .doc-content h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 16px; color: #1e293b; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; }}
        .doc-content h2 {{ font-size: 22px; font-weight: 600; margin-top: 32px; margin-bottom: 12px; color: #1e293b; }}
        .doc-content h3 {{ font-size: 18px; font-weight: 600; margin-top: 24px; margin-bottom: 8px; color: #334155; }}
        .doc-content p {{ margin-bottom: 16px; }}
        .doc-content ul, .doc-content ol {{ margin-bottom: 16px; padding-left: 24px; }}
        .doc-content li {{ margin-bottom: 6px; }}
        .doc-content code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; font-family: 'SF Mono', Monaco, monospace; }}
        .doc-content pre {{ background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; margin-bottom: 16px; }}
        .doc-content pre code {{ background: none; padding: 0; color: inherit; }}
        .doc-content table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; }}
        .doc-content th, .doc-content td {{ border: 1px solid #e2e8f0; padding: 10px 12px; text-align: left; }}
        .doc-content th {{ background: #f8fafc; font-weight: 600; }}
        .doc-content hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }}
        .doc-content a {{ color: #3b82f6; text-decoration: none; }}
        .doc-content a:hover {{ text-decoration: underline; }}
        .doc-path {{ font-size: 12px; color: #94a3b8; margin-bottom: 20px; padding: 8px 12px; background: #f8fafc; border-radius: 6px; font-family: 'SF Mono', Monaco, monospace; }}
        .sidebar h2 {{ font-size: 11px; text-transform: uppercase; color: #94a3b8; margin-bottom: 12px; letter-spacing: 0.5px; font-weight: 600; }}
        .level-group {{ margin-bottom: 16px; }}
        .level-title {{ font-size: 11px; color: #64748b; margin-bottom: 6px; padding: 4px 8px; background: #f1f5f9; border-radius: 4px; font-weight: 500; }}
        .doc-item {{ padding: 8px 12px; margin: 2px 0; border-radius: 6px; cursor: pointer; font-size: 13px; transition: all 0.15s; }}
        .doc-item:hover {{ background: #f1f5f9; }}
        .doc-item.selected {{ background: #3b82f6; color: white; }}
        .doc-item .path {{ font-size: 10px; color: #94a3b8; margin-top: 2px; }}
        .doc-item.selected .path {{ color: rgba(255,255,255,0.7); }}
        .doc-item.viewing {{ background: #dbeafe; }}
        .doc-item.viewing.selected {{ background: #3b82f6; }}
        .legend {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e2e8f0; }}
        .legend-item {{ display: flex; align-items: center; margin: 6px 0; font-size: 12px; color: #64748b; }}
        .legend-color {{ width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }}
        .node {{ cursor: pointer; transition: opacity 0.2s; }}
        .flowchart-link {{ transition: opacity 0.2s; }}
        .edgeLabel {{ transition: opacity 0.2s; }}
        .instructions {{ margin-top: 20px; padding: 12px; background: #f1f5f9; border-radius: 6px; font-size: 11px; color: #64748b; line-height: 1.6; }}
        .instructions strong {{ color: #475569; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>Documents</h2>
            <div id="doc-list"></div>
            <div class="legend">
                <h2>Legend</h2>
                <div class="legend-item"><span class="legend-color" style="background:#22c55e"></span>Independent</div>
                <div class="legend-item"><span class="legend-color" style="background:#3b82f6"></span>Level 1</div>
                <div class="legend-item"><span class="legend-color" style="background:#f59e0b"></span>Level 2</div>
                <div class="legend-item"><span class="legend-color" style="background:#ec4899"></span>Level 3+</div>
            </div>
            <div class="instructions">
                <strong>Tips:</strong><br>
                Click sidebar item to view doc.<br>
                Click graph node to highlight.
            </div>
        </div>
        <div class="main">
            <div class="header">
                <div class="header-top">
                    <h1 id="page-title">Dependency Graph</h1>
                    <div class="tabs">
                        <div class="tab active" data-tab="graph">Graph</div>
                        <div class="tab" data-tab="doc">Doc Preview</div>
                    </div>
                </div>
                <div class="stats">
                    <span id="stat-total"></span>
                    <span id="stat-independent"></span>
                    <span id="stat-depth"></span>
                    <span id="stat-circular"></span>
                </div>
            </div>
            <div class="content">
                <div class="panel graph-panel" id="graph-panel">
                    <div class="mermaid" id="graph"></div>
                </div>
                <div class="panel doc-panel hidden empty" id="doc-panel">
                    Select a document to preview
                </div>
            </div>
        </div>
    </div>
    <script>
        const graphData = {graph_json};
        const levelColors = ['#22c55e', '#3b82f6', '#f59e0b', '#ec4899', '#a855f7', '#06b6d4'];
        let currentTab = 'graph';
        let currentDoc = null;

        function switchTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
            document.getElementById('graph-panel').classList.toggle('hidden', tab !== 'graph');
            document.getElementById('doc-panel').classList.toggle('hidden', tab !== 'doc');
            if (tab === 'graph') {{
                document.getElementById('page-title').textContent = 'Dependency Graph';
            }}
        }}

        document.querySelectorAll('.tab').forEach(tab => {{
            tab.addEventListener('click', () => switchTab(tab.dataset.tab));
        }});

        async function loadDoc(path) {{
            currentDoc = path;
            const docPanel = document.getElementById('doc-panel');
            docPanel.classList.remove('empty');
            docPanel.innerHTML = '<div style="color:#94a3b8">Loading...</div>';
            switchTab('doc');
            try {{
                const res = await fetch('/doc?path=' + encodeURIComponent(path));
                if (!res.ok) throw new Error('Failed to load');
                const md = await res.text();
                const html = marked.parse(md);
                docPanel.innerHTML = '<div class="doc-path">' + path + '</div><div class="doc-content">' + html + '</div>';
                const node = graphData.nodes.find(n => n.path === path);
                document.getElementById('page-title').textContent = node ? node.name : path;
                document.querySelectorAll('.doc-item').forEach(el => {{
                    const itemPath = graphData.nodes.find(n => n.id === el.dataset.nodeId)?.path;
                    el.classList.toggle('viewing', itemPath === path);
                }});
            }} catch (e) {{
                docPanel.innerHTML = '<div style="color:#ef4444">Failed to load document</div>';
            }}
        }}

        function buildMermaidDef() {{
            let lines = ['flowchart TB'];
            const levelGroups = {{}};
            graphData.nodes.forEach(n => {{
                if (!levelGroups[n.level]) levelGroups[n.level] = [];
                levelGroups[n.level].push(n);
            }});
            Object.keys(levelGroups).sort((a,b) => a-b).forEach(level => {{
                const nodes = levelGroups[level];
                const label = level == 0 ? 'Independent' : 'Level ' + level;
                const color = levelColors[level % levelColors.length];
                lines.push('    subgraph L' + level + '[' + label + ']');
                lines.push('        style L' + level + ' fill:#fff,stroke:' + color + ',stroke-width:2px');
                nodes.forEach(n => {{
                    lines.push('        ' + n.id + '["' + n.name + '"]');
                }});
                lines.push('    end');
            }});
            graphData.edges.forEach((e, i) => {{
                if (e.circular) {{
                    lines.push('    ' + e.from + ' -.->|circular| ' + e.to);
                }} else {{
                    lines.push('    ' + e.from + ' --> ' + e.to);
                }}
            }});
            graphData.nodes.forEach(n => {{
                const color = levelColors[n.level % levelColors.length];
                lines.push('    style ' + n.id + ' fill:' + color + ',stroke:' + color + ',color:#fff');
            }});
            return lines.join('\\n');
        }}

        function buildDocList() {{
            const container = document.getElementById('doc-list');
            const levelGroups = {{}};
            graphData.nodes.forEach(n => {{
                if (!levelGroups[n.level]) levelGroups[n.level] = [];
                levelGroups[n.level].push(n);
            }});
            Object.keys(levelGroups).sort((a,b) => a-b).forEach(level => {{
                const group = document.createElement('div');
                group.className = 'level-group';
                const title = document.createElement('div');
                title.className = 'level-title';
                const label = level == 0 ? 'Independent' : 'Level ' + level;
                title.textContent = label + ' (' + levelGroups[level].length + ')';
                group.appendChild(title);
                levelGroups[level].sort((a,b) => a.name.localeCompare(b.name)).forEach(n => {{
                    const item = document.createElement('div');
                    item.className = 'doc-item';
                    item.dataset.nodeId = n.id;
                    item.dataset.path = n.path;
                    item.innerHTML = '<div>' + n.name + '</div><div class="path">' + n.path + '</div>';
                    item.addEventListener('click', () => {{
                        highlightNode(n.id);
                        loadDoc(n.path);
                    }});
                    group.appendChild(item);
                }});
                container.appendChild(group);
            }});
        }}

        function updateStats() {{
            document.getElementById('stat-total').textContent = 'Total: ' + graphData.stats.total;
            document.getElementById('stat-independent').textContent = 'Independent: ' + graphData.stats.independent;
            document.getElementById('stat-depth').textContent = 'Max depth: ' + graphData.stats.max_depth;
            if (graphData.stats.circular > 0) {{
                document.getElementById('stat-circular').textContent = 'Circular: ' + graphData.stats.circular;
                document.getElementById('stat-circular').style.color = '#f59e0b';
            }}
        }}

        let selectedNode = null;
        let edgeElements = [];

        function indexEdges() {{
            edgeElements = Array.from(document.querySelectorAll('.flowchart-link'));
        }}

        function getConnectedNodes(nodeId) {{
            const connected = new Set([nodeId]);
            graphData.edges.forEach(e => {{
                if (e.from === nodeId) connected.add(e.to);
                if (e.to === nodeId) connected.add(e.from);
            }});
            return connected;
        }}

        function getConnectedEdgeIndices(nodeId) {{
            const indices = [];
            graphData.edges.forEach((e, i) => {{
                if (e.from === nodeId || e.to === nodeId) {{
                    indices.push(i);
                }}
            }});
            return indices;
        }}

        function highlightNode(nodeId) {{
            if (selectedNode === nodeId) {{
                resetHighlight();
                return;
            }}
            selectedNode = nodeId;
            const connected = getConnectedNodes(nodeId);
            const connectedEdgeIndices = new Set(getConnectedEdgeIndices(nodeId));
            document.querySelectorAll('.node').forEach(el => {{
                const id = el.id.split('-')[1];
                el.style.opacity = connected.has(id) ? '1' : '0.06';
            }});
            edgeElements.forEach((el, i) => {{
                el.style.opacity = connectedEdgeIndices.has(i) ? '1' : '0';
            }});
            document.querySelectorAll('.edgeLabel').forEach(el => {{
                el.style.opacity = '0';
            }});
            document.querySelectorAll('.doc-item').forEach(el => {{
                el.classList.toggle('selected', el.dataset.nodeId === nodeId);
            }});
        }}

        function resetHighlight() {{
            selectedNode = null;
            document.querySelectorAll('.node').forEach(el => {{
                el.style.opacity = '1';
            }});
            edgeElements.forEach(el => {{
                el.style.opacity = '1';
            }});
            document.querySelectorAll('.edgeLabel').forEach(el => {{
                el.style.opacity = '1';
            }});
            document.querySelectorAll('.doc-item').forEach(el => {{
                el.classList.remove('selected');
            }});
        }}

        mermaid.initialize({{
            startOnLoad: false,
            theme: 'base',
            themeVariables: {{
                background: '#ffffff',
                primaryColor: '#3b82f6',
                lineColor: '#94a3b8',
            }},
            flowchart: {{ curve: 'basis', padding: 20 }},
            securityLevel: 'loose',
        }});

        async function renderGraph() {{
            const def = buildMermaidDef();
            const {{ svg }} = await mermaid.render('mermaid-graph', def);
            document.getElementById('graph').innerHTML = svg;
            indexEdges();
            document.querySelectorAll('.node').forEach(el => {{
                el.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const nodeId = el.id.split('-')[1];
                    highlightNode(nodeId);
                }});
                el.addEventListener('dblclick', (e) => {{
                    e.stopPropagation();
                    const nodeId = el.id.split('-')[1];
                    const node = graphData.nodes.find(n => n.id === nodeId);
                    if (node) loadDoc(node.path);
                }});
            }});
            document.querySelector('.graph-panel').addEventListener('click', (e) => {{
                if (e.target.closest('.node') === null) {{
                    resetHighlight();
                }}
            }});
        }}

        buildDocList();
        updateStats();
        renderGraph();
    </script>
</body>
</html>"""


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, html_content: str, repo_root: Path, **kwargs):
        self.html_content = html_content
        self.repo_root = repo_root
        super().__init__(*args, **kwargs)

    def do_GET(self):
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.html_content.encode())
        elif parsed.path == "/doc":
            params = parse_qs(parsed.query)
            doc_path = params.get("path", [None])[0]
            if doc_path:
                full_path = self.repo_root / doc_path
                if full_path.exists() and full_path.suffix == ".md":
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(full_path.read_text(encoding="utf-8").encode("utf-8"))
                else:
                    self.send_error(404, "Document not found")
            else:
                self.send_error(400, "Missing path parameter")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def run(docs_path: Path, port: int = 8420) -> int:
    config = load_config()
    docs_path = docs_path.resolve()
    repo_root = find_repo_root(docs_path)
    graph_data = build_graph_data(docs_path, config, repo_root)
    html_content = generate_html(graph_data)

    handler = lambda *args, **kwargs: PreviewHandler(*args, html_content=html_content, repo_root=repo_root, **kwargs)

    class ReuseAddrTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReuseAddrTCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}"
        print(f"Serving docs preview at {url}")
        print("Press Ctrl+C to stop")
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped")
    return 0
