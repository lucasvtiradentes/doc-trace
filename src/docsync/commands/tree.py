from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from docsync.core.config import Config, find_repo_root
from docsync.core.parser import parse_doc


class DependencyTree(NamedTuple):
    levels: list[list[Path]]
    circular: list[tuple[Path, Path]]
    doc_deps: dict[Path, list[Path]]


def build_dependency_tree(docs_path: Path, config: Config, repo_root: Path | None = None) -> DependencyTree:
    if repo_root is None:
        repo_root = find_repo_root(docs_path)
    doc_deps = _build_doc_dependencies(docs_path, repo_root)
    levels, circular = _compute_levels(doc_deps)
    return DependencyTree(levels=levels, circular=circular, doc_deps=doc_deps)


def _build_doc_dependencies(docs_path: Path, repo_root: Path) -> dict[Path, list[Path]]:
    doc_deps: dict[Path, list[Path]] = defaultdict(list)
    doc_files = list(docs_path.rglob("*.md"))
    for doc_file in doc_files:
        try:
            parsed = parse_doc(doc_file)
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


def format_tree(tree: DependencyTree, repo_root: Path) -> str:
    lines = []
    for i, level_docs in enumerate(tree.levels):
        if not level_docs:
            continue
        if i == 0:
            lines.append(f"Level 0 - Independent ({len(level_docs)}):")
        else:
            lines.append(f"\nLevel {i} ({len(level_docs)}):")
        for doc in level_docs:
            rel_path = doc.relative_to(repo_root)
            deps = tree.doc_deps.get(doc, [])
            if deps:
                dep_names = ", ".join(str(d.relative_to(repo_root)) for d in deps)
                lines.append(f"  {rel_path}")
                lines.append(f"    └── depends on: {dep_names}")
            else:
                lines.append(f"  {rel_path}")
    if tree.circular:
        lines.append("\nCircular dependencies (warning):")
        for src, dst in tree.circular:
            src_rel = src.relative_to(repo_root)
            dst_rel = dst.relative_to(repo_root)
            lines.append(f"  {src_rel} <-> {dst_rel}")
    return "\n".join(lines)


def run(docs_path: Path) -> int:
    from docsync.core.config import load_config

    config = load_config()
    docs_path = docs_path.resolve()
    repo_root = find_repo_root(docs_path)
    tree = build_dependency_tree(docs_path, config, repo_root)
    print(format_tree(tree, repo_root))
    return 0
