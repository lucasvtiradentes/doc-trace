import subprocess
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from docsync.config import Config
from docsync.parser import parse_doc


class CascadeResult(NamedTuple):
    affected_docs: list[Path]
    direct_hits: list[Path]
    cascade_hits: list[Path]
    circular_refs: list[tuple[Path, Path]]


def find_affected_docs(
    docs_path: Path, commit_ref: str, config: Config, repo_root: Path | None = None
) -> CascadeResult:
    if repo_root is None:
        repo_root = _find_repo_root(docs_path)
    changed_files = _get_changed_files(commit_ref, repo_root)
    if not changed_files:
        return CascadeResult([], [], [], [])
    source_to_docs, doc_to_docs = _build_indexes(docs_path, repo_root)
    direct_hits = _find_direct_hits(changed_files, source_to_docs)
    cascade_hits, circular_refs = _cascade(direct_hits, doc_to_docs, config.cascade_depth_limit)
    all_affected = list(set(direct_hits) | set(cascade_hits))
    return CascadeResult(
        affected_docs=all_affected, direct_hits=direct_hits, cascade_hits=cascade_hits, circular_refs=circular_refs
    )


def _get_changed_files(commit_ref: str, repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", commit_ref], capture_output=True, text=True, check=True, cwd=repo_root
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError:
        return []


def _build_indexes(docs_path: Path, repo_root: Path) -> tuple[dict[str, list[Path]], dict[Path, list[Path]]]:
    source_to_docs: dict[str, list[Path]] = defaultdict(list)
    doc_to_docs: dict[Path, list[Path]] = defaultdict(list)
    doc_files = list(docs_path.rglob("*.md"))
    for doc_file in doc_files:
        try:
            parsed = parse_doc(doc_file)
        except Exception:
            continue
        for ref in parsed.related_sources:
            source_to_docs[ref.path].append(doc_file)
        for ref in parsed.related_docs:
            ref_path = repo_root / ref.path
            if ref_path.exists():
                doc_to_docs[ref_path].append(doc_file)
    return source_to_docs, doc_to_docs


def _find_direct_hits(changed_files: list[str], source_to_docs: dict[str, list[Path]]) -> list[Path]:
    hits = []
    for changed in changed_files:
        if changed in source_to_docs:
            hits.extend(source_to_docs[changed])
    return list(set(hits))


def _cascade(
    initial_docs: list[Path], doc_to_docs: dict[Path, list[Path]], depth_limit: int | None
) -> tuple[list[Path], list[tuple[Path, Path]]]:
    cascade_hits = []
    circular_refs = []
    visited = set(initial_docs)
    current_level = set(initial_docs)
    depth = 0
    while current_level:
        if depth_limit is not None and depth >= depth_limit:
            break
        next_level = set()
        for doc in current_level:
            for referencing_doc in doc_to_docs.get(doc, []):
                if referencing_doc in visited:
                    if referencing_doc not in initial_docs:
                        circular_refs.append((doc, referencing_doc))
                    continue
                visited.add(referencing_doc)
                cascade_hits.append(referencing_doc)
                next_level.add(referencing_doc)
        current_level = next_level
        depth += 1
    return cascade_hits, circular_refs


def _find_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()
