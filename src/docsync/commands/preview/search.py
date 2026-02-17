from __future__ import annotations

from pathlib import Path


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
