from __future__ import annotations

import http.server
import json
import socketserver
import subprocess
import threading
import webbrowser
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from docsync.core.config import Config, find_repo_root, load_config
from docsync.core.parser import parse_doc


class DependencyTree(NamedTuple):
    levels: list[list[Path]]
    circular: list[tuple[Path, Path]]
    doc_deps: dict[Path, list[Path]]


def build_dependency_tree(docs_path: Path, config: Config, repo_root: Path | None = None) -> DependencyTree:
    if repo_root is None:
        repo_root = find_repo_root(docs_path)
    doc_deps = _build_doc_dependencies(docs_path, repo_root, config)
    levels, circular = _compute_levels(doc_deps)
    return DependencyTree(levels=levels, circular=circular, doc_deps=doc_deps)


def _build_doc_dependencies(docs_path: Path, repo_root: Path, config: Config) -> dict[Path, list[Path]]:
    doc_deps: dict[Path, list[Path]] = defaultdict(list)
    doc_files = list(docs_path.rglob("*.md"))
    for doc_file in doc_files:
        try:
            parsed = parse_doc(doc_file, config.metadata)
        except Exception:
            continue
        for ref in parsed.related_docs:
            ref_path = repo_root / ref.path
            if ref_path.exists():
                doc_deps[doc_file].append(ref_path)
        if doc_file not in doc_deps:
            doc_deps[doc_file] = []
    return dict(doc_deps)


def _compute_levels(doc_deps: dict[Path, list[Path]]) -> tuple[list[list[Path]], list[tuple[Path, Path]]]:
    all_docs = set(doc_deps.keys())
    assigned: dict[Path, int] = {}
    circular: list[tuple[Path, Path]] = []

    def get_level(doc: Path, visiting: set[Path]) -> int:
        if doc in assigned:
            return assigned[doc]
        if doc in visiting:
            return -1
        if doc not in doc_deps:
            assigned[doc] = 0
            return 0
        deps = doc_deps[doc]
        if not deps:
            assigned[doc] = 0
            return 0
        visiting.add(doc)
        max_dep_level = -1
        for dep in deps:
            dep_level = get_level(dep, visiting)
            if dep_level == -1:
                circular.append((doc, dep))
                continue
            max_dep_level = max(max_dep_level, dep_level)
        visiting.remove(doc)
        level = max_dep_level + 1 if max_dep_level >= 0 else 0
        assigned[doc] = level
        return level

    for doc in all_docs:
        get_level(doc, set())

    max_level = max(assigned.values()) if assigned else 0
    levels: list[list[Path]] = [[] for _ in range(max_level + 1)]
    for doc, level in assigned.items():
        levels[level].append(doc)

    for level_docs in levels:
        level_docs.sort()

    return levels, circular


def get_file_history(repo_root: Path, file_path: str, limit: int = 20) -> list[dict]:
    try:
        result = subprocess.run(
            ["git", "log", f"-{limit}", "--pretty=format:%H|%h|%s|%ai|%an", "--", file_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []
        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|", 4)
            if len(parts) >= 5:
                commits.append({
                    "hash": parts[0],
                    "short": parts[1],
                    "message": parts[2],
                    "date": parts[3],
                    "author": parts[4],
                })
        return commits
    except Exception:
        return []


def search_docs(repo_root: Path, docs_path: Path, query: str) -> list[dict]:
    results = []
    query_lower = query.lower()
    for md_file in docs_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            content_lower = content.lower()
            if query_lower in content_lower:
                rel_path = str(md_file.relative_to(repo_root))
                lines = content.split("\n")
                matches = []
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        matches.append({"line": i + 1, "text": line.strip()[:100]})
                        if len(matches) >= 3:
                            break
                results.append({"path": rel_path, "name": md_file.stem, "matches": matches})
        except Exception:
            pass
    return results


def get_file_at_commit(repo_root: Path, file_path: str, commit: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{file_path}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception:
        return None

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
    def __init__(self, *args, html_content: str, repo_root: Path, docs_path: Path, **kwargs):
        self.html_content = html_content
        self.repo_root = repo_root
        self.docs_path = docs_path
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
            commit = params.get("commit", [None])[0]
            if doc_path:
                full_path = self.repo_root / doc_path
                if full_path.suffix == ".md":
                    if commit:
                        content = get_file_at_commit(self.repo_root, doc_path, commit)
                        if content is not None:
                            self.send_response(200)
                            self.send_header("Content-type", "text/plain; charset=utf-8")
                            self.end_headers()
                            self.wfile.write(content.encode("utf-8"))
                        else:
                            self.send_error(404, "Version not found")
                    elif full_path.exists():
                        self.send_response(200)
                        self.send_header("Content-type", "text/plain; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(full_path.read_text(encoding="utf-8").encode("utf-8"))
                    else:
                        self.send_error(404, "Document not found")
                else:
                    self.send_error(404, "Document not found")
            else:
                self.send_error(400, "Missing path parameter")
        elif parsed.path == "/history":
            params = parse_qs(parsed.query)
            doc_path = params.get("path", [None])[0]
            if doc_path:
                history = get_file_history(self.repo_root, doc_path)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(history).encode("utf-8"))
            else:
                self.send_error(400, "Missing path parameter")
        elif parsed.path == "/search":
            params = parse_qs(parsed.query)
            query = params.get("q", [None])[0]
            if query and len(query) >= 2:
                results = search_docs(self.repo_root, self.docs_path, query)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(results).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'[]')
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

    handler = lambda *args, **kwargs: PreviewHandler(*args, html_content=html_content, repo_root=repo_root, docs_path=docs_path, **kwargs)

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
