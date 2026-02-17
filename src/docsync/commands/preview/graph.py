from __future__ import annotations

import json
from pathlib import Path

from docsync.commands.preview.tree import build_dependency_tree
from docsync.core.config import Config

TEMPLATE_PATH = Path(__file__).parent / "template.html"


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
        nodes.append(
            {
                "id": node_id,
                "path": rel_path,
                "name": doc.stem,
                "level": level,
            }
        )
    for doc, deps in tree.doc_deps.items():
        for dep in deps:
            if dep in node_ids:
                edges.append(
                    {
                        "from": node_ids[dep],
                        "to": node_ids[doc],
                    }
                )
    for src, dst in tree.circular:
        if src in node_ids and dst in node_ids:
            edges.append(
                {
                    "from": node_ids[src],
                    "to": node_ids[dst],
                    "circular": True,
                }
            )
    levels_info = []
    for i, level_docs in enumerate(tree.levels):
        levels_info.append(
            {
                "level": i,
                "count": len(level_docs),
                "label": "Independent" if i == 0 else f"Level {i}",
            }
        )
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
