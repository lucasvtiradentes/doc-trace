from __future__ import annotations

import http.server
import json
import socketserver
import threading
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from doctrace.commands.preview.graph import build_graph_data, generate_html
from doctrace.commands.preview.search import search_docs
from doctrace.core.config import find_repo_root, load_config
from doctrace.core.constants import DEFAULT_PREVIEW_PORT
from doctrace.core.git import get_file_at_commit, get_file_history


class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, html_content: str, repo_root: Path, docs_path: Path, **kwargs):
        self.html_content = html_content
        self.repo_root = repo_root
        self.docs_path = docs_path
        super().__init__(*args, **kwargs)

    def _is_safe_path(self, doc_path: str) -> bool:
        full_path = (self.repo_root / doc_path).resolve()
        return full_path.is_relative_to(self.repo_root)

    def do_GET(self):
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
                if not self._is_safe_path(doc_path):
                    self.send_error(403, "Forbidden")
                    return
                full_path = (self.repo_root / doc_path).resolve()
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
                if not self._is_safe_path(doc_path):
                    self.send_error(403, "Forbidden")
                    return
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
                self.wfile.write(b"[]")
        else:
            self.send_error(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/doc":
            params = parse_qs(parsed.query)
            doc_path = params.get("path", [None])[0]
            if doc_path:
                if not self._is_safe_path(doc_path):
                    self.send_error(403, "Forbidden")
                    return
                full_path = (self.repo_root / doc_path).resolve()
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


def run(docs_path: Path, port: int = DEFAULT_PREVIEW_PORT) -> int:
    config = load_config()
    docs_path = docs_path.resolve()
    repo_root = find_repo_root(docs_path)
    graph_data = build_graph_data(docs_path, config, repo_root)
    html_content = generate_html(graph_data)

    def handler(*args, **kwargs):
        return PreviewHandler(*args, html_content=html_content, repo_root=repo_root, docs_path=docs_path, **kwargs)

    with ReuseAddrTCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}"
        print(f"Serving docs preview at {url}")
        print("Press Ctrl+C to stop")
        timer = threading.Timer(0.5, lambda: webbrowser.open(url))
        timer.start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped")
        finally:
            timer.cancel()
    return 0
