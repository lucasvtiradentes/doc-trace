from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

from doctrace.core.constants import MARKDOWN_GLOB

if TYPE_CHECKING:
    from doctrace.core.config import Config, MetadataConfig

LIST_ITEM_YAML = re.compile(r"^\s*-\s+([^:]+?):\s*(.*)$")


class RefEntry(NamedTuple):
    path: str
    description: str
    line_number: int


class ParsedDoc(NamedTuple):
    required_docs: list[RefEntry]
    related_docs: list[RefEntry]
    sources: list[RefEntry]


def parse_doc(filepath: Path, metadata_config: MetadataConfig | None = None) -> ParsedDoc:
    from doctrace.core.config import MetadataConfig

    if metadata_config is None:
        metadata_config = MetadataConfig({})

    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()
    metadata_lines = _get_frontmatter_section(lines)

    required_docs_pattern = re.compile(rf"^{re.escape(metadata_config.required_docs_key)}:\s*$", re.IGNORECASE)
    related_docs_pattern = re.compile(rf"^{re.escape(metadata_config.related_docs_key)}:\s*$", re.IGNORECASE)
    sources_pattern = re.compile(rf"^{re.escape(metadata_config.sources_key)}:\s*$", re.IGNORECASE)

    required_docs = _extract_section(metadata_lines, required_docs_pattern)
    related_docs = _extract_section(metadata_lines, related_docs_pattern)
    sources = _extract_section(metadata_lines, sources_pattern)
    return ParsedDoc(required_docs=required_docs, related_docs=related_docs, sources=sources)


def _get_frontmatter_section(lines: list[str]) -> list[tuple[int, str]]:
    if not lines or lines[0].strip() != "---":
        return []
    end_line = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_line = i
            break
    if end_line is None:
        return []
    return [(i + 1, line) for i, line in enumerate(lines) if 0 < i < end_line]


def _extract_section(lines: list[tuple[int, str]], header_pattern: re.Pattern) -> list[RefEntry]:
    entries = []
    in_section = False
    for line_num, line in lines:
        if header_pattern.match(line):
            in_section = True
            continue
        if in_section:
            if not line.strip():
                continue
            if line.strip().startswith("-"):
                match = LIST_ITEM_YAML.match(line)
                if match:
                    path = match.group(1).strip()
                    desc = match.group(2).strip() if match.group(2) else ""
                    entries.append(RefEntry(path=path, description=desc, line_number=line_num))
            else:
                break
    return entries


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
