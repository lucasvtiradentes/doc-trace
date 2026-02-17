from __future__ import annotations

import http.server
import json
import socketserver
import threading
import webbrowser
from pathlib import Path

from docsync.commands.tree import build_dependency_tree
from docsync.core.config import Config, find_repo_root, load_config

TEMPLATE_PATH = Path(__file__).parent / "preview_template.html"


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
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    graph_json = json.dumps(graph_data)
    return template.replace('"__GRAPH_DATA__"', graph_json)


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

    def do_POST(self):
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(self.path)
        if parsed.path == "/doc":
            params = parse_qs(parsed.query)
            doc_path = params.get("path", [None])[0]
            if doc_path:
                full_path = self.repo_root / doc_path
                if full_path.exists() and full_path.suffix == ".md":
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length).decode("utf-8")
                    full_path.write_text(body, encoding="utf-8")
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"ok":true}')
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
