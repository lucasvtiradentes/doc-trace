from __future__ import annotations

import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from docsync.core.config import Config, find_repo_root
from docsync.core.lock import load_lock
from docsync.core.parser import parse_doc


class AffectedResult(NamedTuple):
    affected_docs: list[Path]
    direct_hits: list[Path]
    indirect_hits: list[Path]
    circular_refs: list[tuple[Path, Path]]


def resolve_commit_ref(
    repo_root: Path, since_lock: bool = False, last: int | None = None, base_branch: str | None = None
) -> str:
    options_selected = int(since_lock) + int(last is not None) + int(base_branch is not None)
    if options_selected != 1:
        raise ValueError("choose exactly one scope: --since-lock, --last <N>, or --base-branch <branch>")
    if since_lock:
        lock = load_lock(repo_root)
        if not lock.last_analyzed_commit:
            raise ValueError("lock.json has no last_analyzed_commit; cannot use --since-lock")
        return lock.last_analyzed_commit
    if last is not None:
        if last <= 0:
            raise ValueError("--last must be greater than 0")
        return f"HEAD~{last}"
    assert base_branch is not None
    try:
        result = subprocess.run(
            ["git", "merge-base", "HEAD", base_branch], capture_output=True, text=True, check=True, cwd=repo_root
        )
        commit = result.stdout.strip()
        if not commit:
            raise ValueError(f"could not resolve merge-base with branch '{base_branch}'")
        return commit
    except subprocess.CalledProcessError as e:
        msg = e.stderr.strip() if e.stderr else f"could not resolve merge-base with branch '{base_branch}'"
        raise ValueError(msg) from e


def find_affected_docs(
    docs_path: Path, commit_ref: str, config: Config, repo_root: Path | None = None
) -> AffectedResult:
    if repo_root is None:
        repo_root = find_repo_root(docs_path)
    changed_files = _get_changed_files(commit_ref, repo_root)
    return _find_affected_docs_for_changes(docs_path, changed_files, config, repo_root)


def _find_affected_docs_for_changes(
    docs_path: Path, changed_files: list[str], config: Config, repo_root: Path
) -> AffectedResult:
    if not changed_files:
        return AffectedResult([], [], [], [])
    source_to_docs, doc_to_docs = _build_indexes(docs_path, repo_root, config)
    direct_hits = _find_direct_hits(changed_files, source_to_docs)
    indirect_hits, circular_refs = _propagate(direct_hits, doc_to_docs, config.affected_depth_limit)
    all_affected = list(set(direct_hits) | set(indirect_hits))
    return AffectedResult(
        affected_docs=all_affected, direct_hits=direct_hits, indirect_hits=indirect_hits, circular_refs=circular_refs
    )


def _get_changed_files(commit_ref: str, repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", commit_ref], capture_output=True, text=True, check=True, cwd=repo_root
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def _build_indexes(
    docs_path: Path, repo_root: Path, config: Config
) -> tuple[dict[str, list[Path]], dict[Path, list[Path]]]:
    source_to_docs: dict[str, list[Path]] = defaultdict(list)
    doc_to_docs: dict[Path, list[Path]] = defaultdict(list)
    doc_files = list(docs_path.rglob("*.md"))
    for doc_file in doc_files:
        try:
            parsed = parse_doc(doc_file, config.metadata)
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
        for source_ref, docs in source_to_docs.items():
            if source_ref.endswith("/") and changed.startswith(source_ref):
                hits.extend(docs)
    return list(set(hits))


def _propagate(
    initial_docs: list[Path], doc_to_docs: dict[Path, list[Path]], depth_limit: int | None
) -> tuple[list[Path], list[tuple[Path, Path]]]:
    indirect_hits = []
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
                indirect_hits.append(referencing_doc)
                next_level.add(referencing_doc)
        current_level = next_level
        depth += 1
    return indirect_hits, circular_refs


def run(
    docs_path: Path,
    since_lock: bool = False,
    last: int | None = None,
    base_branch: str | None = None,
    show_changed_files: bool = False,
) -> int:
    from docsync.core.config import load_config

    config = load_config()
    repo_root = find_repo_root(docs_path)
    try:
        commit_ref = resolve_commit_ref(repo_root, since_lock, last, base_branch)
    except ValueError as e:
        print(f"Scope error: {e}", file=sys.stderr)
        return 2

    changed_files = _get_changed_files(commit_ref, repo_root)
    if show_changed_files:
        print(f"Changed files ({len(changed_files)}):")
        for changed_file in changed_files:
            print(f"  {changed_file}")
        print("")

    result = _find_affected_docs_for_changes(docs_path, changed_files, config, repo_root)
    if not result.affected_docs:
        print("No docs affected")
        return 0
    print(f"Direct hits ({len(result.direct_hits)}):")
    for doc in result.direct_hits:
        print(f"  {doc}")
    if result.indirect_hits:
        print(f"\nIndirect hits ({len(result.indirect_hits)}):")
        for doc in result.indirect_hits:
            print(f"  {doc}")
    if result.circular_refs:
        print("\nWarning: circular refs detected:")
        for src, dst in result.circular_refs:
            print(f"  {src} <-> {dst}")
    return 0
