from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from doctrace.core.config import Config
from doctrace.core.constants import MARKDOWN_GLOB
from doctrace.core.parser import ParsedDoc, parse_doc


class DocIndex(NamedTuple):
    parsed_cache: dict[Path, ParsedDoc]
    source_to_docs: dict[str, list[Path]]
    forward_deps: dict[Path, list[Path]]
    reverse_deps: dict[Path, list[Path]]


def build_doc_index(docs_path: Path, config: Config, repo_root: Path) -> DocIndex:
    parsed_cache: dict[Path, ParsedDoc] = {}
    source_to_docs: dict[str, list[Path]] = defaultdict(list)
    forward_deps: dict[Path, list[Path]] = defaultdict(list)
    reverse_deps: dict[Path, list[Path]] = defaultdict(list)

    doc_files = [f.resolve() for f in docs_path.rglob(MARKDOWN_GLOB)]
    for doc_file in doc_files:
        try:
            parsed = parse_doc(doc_file, config.metadata)
        except (OSError, UnicodeDecodeError, ValueError):
            continue

        parsed_cache[doc_file] = parsed

        for ref in parsed.sources:
            source_to_docs[ref.path].append(doc_file)

        for ref in parsed.required_docs:
            ref_path = repo_root / ref.path
            if ref_path.exists():
                forward_deps[doc_file].append(ref_path)
                reverse_deps[ref_path].append(doc_file)

        forward_deps.setdefault(doc_file, [])

    return DocIndex(
        parsed_cache=dict(parsed_cache),
        source_to_docs=dict(source_to_docs),
        forward_deps=dict(forward_deps),
        reverse_deps=dict(reverse_deps),
    )


class LevelResult(NamedTuple):
    levels: list[list[Path]]
    circular: list[tuple[Path, Path]]


def compute_levels(doc_deps: dict[Path, list[Path]]) -> LevelResult:
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

    return LevelResult(levels=levels, circular=circular)


class DependencyTree(NamedTuple):
    levels: list[list[Path]]
    circular: list[tuple[Path, Path]]
    doc_deps: dict[Path, list[Path]]
    index: DocIndex


def build_dependency_tree(docs_path: Path, config: Config, repo_root: Path) -> DependencyTree:
    index = build_doc_index(docs_path, config, repo_root)
    level_result = compute_levels(index.forward_deps)
    return DependencyTree(
        levels=level_result.levels,
        circular=level_result.circular,
        doc_deps=index.forward_deps,
        index=index,
    )
