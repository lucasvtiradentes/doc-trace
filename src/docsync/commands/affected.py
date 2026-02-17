from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple

from docsync.core.config import Config, find_repo_root
from docsync.core.git import get_changed_files, get_merge_base
from docsync.core.lock import load_lock
from docsync.core.parser import parse_doc


class AffectedResult(NamedTuple):
    affected_docs: list[Path]
    direct_hits: list[Path]
    indirect_hits: list[Path]
    circular_refs: list[tuple[Path, Path]]
    matches: dict[str, list[Path]]
    indirect_chains: dict[Path, Path]


def resolve_commit_ref(
    repo_root: Path,
    since_lock: bool = False,
    last: int | None = None,
    base_branch: str | None = None,
    since: str | None = None,
) -> str:
    options_selected = int(since_lock) + int(last is not None) + int(base_branch is not None) + int(since is not None)
    if options_selected != 1:
        raise ValueError("choose exactly one scope: --since-lock, --last <N>, --base-branch <branch>, or --since <ref>")
    if since_lock:
        lock = load_lock(repo_root)
        if not lock.last_analyzed_commit:
            raise ValueError("lock.json has no last_analyzed_commit; cannot use --since-lock")
        return lock.last_analyzed_commit
    if last is not None:
        if last <= 0:
            raise ValueError("--last must be greater than 0")
        return f"HEAD~{last}"
    if base_branch is not None:
        commit = get_merge_base(base_branch, repo_root)
        if not commit:
            raise ValueError(f"could not resolve merge-base with branch '{base_branch}'")
        return commit
    assert since is not None
    return since


def find_affected_docs(
    docs_path: Path, commit_ref: str, config: Config, repo_root: Path | None = None
) -> AffectedResult:
    if repo_root is None:
        repo_root = find_repo_root(docs_path)
    changed_files = get_changed_files(commit_ref, repo_root)
    return _find_affected_docs_for_changes(docs_path, changed_files, config, repo_root)


def _find_affected_docs_for_changes(
    docs_path: Path, changed_files: list[str], config: Config, repo_root: Path
) -> AffectedResult:
    if not changed_files:
        return AffectedResult([], [], [], [], {}, {})
    source_to_docs, doc_to_docs = _build_indexes(docs_path, repo_root, config)
    direct_hits, matches = _find_direct_hits(changed_files, source_to_docs)
    indirect_hits, circular_refs, indirect_chains = _propagate(direct_hits, doc_to_docs, config.affected_depth_limit)
    all_affected = list(set(direct_hits) | set(indirect_hits))
    return AffectedResult(
        affected_docs=all_affected,
        direct_hits=direct_hits,
        indirect_hits=indirect_hits,
        circular_refs=circular_refs,
        matches=matches,
        indirect_chains=indirect_chains,
    )


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


def _find_direct_hits(
    changed_files: list[str], source_to_docs: dict[str, list[Path]]
) -> tuple[list[Path], dict[str, list[Path]]]:
    hits = []
    matches: dict[str, list[Path]] = defaultdict(list)
    for changed in changed_files:
        if changed in source_to_docs:
            hits.extend(source_to_docs[changed])
            matches[changed].extend(source_to_docs[changed])
        for source_ref, docs in source_to_docs.items():
            if source_ref.endswith("/") and changed.startswith(source_ref):
                hits.extend(docs)
                matches[source_ref].extend(docs)
    for key in matches:
        matches[key] = list(set(matches[key]))
    return list(set(hits)), dict(matches)


def _propagate(
    initial_docs: list[Path], doc_to_docs: dict[Path, list[Path]], depth_limit: int | None
) -> tuple[list[Path], list[tuple[Path, Path]], dict[Path, Path]]:
    indirect_hits = []
    circular_refs = []
    indirect_chains: dict[Path, Path] = {}
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
                indirect_chains[referencing_doc] = doc
                next_level.add(referencing_doc)
        current_level = next_level
        depth += 1
    return indirect_hits, circular_refs, indirect_chains


def _get_doc_metadata(docs: list[Path], config: Config, repo_root: Path) -> list[dict[str, Any]]:
    result = []
    for doc_file in docs:
        try:
            abs_path = doc_file if doc_file.is_absolute() else repo_root / doc_file
            parsed = parse_doc(abs_path, config.metadata)
            rel_path = str(abs_path.relative_to(repo_root))
            result.append(
                {
                    "path": rel_path,
                    "related_docs": [ref.path for ref in parsed.related_docs],
                    "related_sources": [ref.path for ref in parsed.related_sources],
                }
            )
        except Exception:
            continue
    return result


def _build_levels(docs: list[dict[str, Any]], repo_root: Path) -> list[list[dict[str, Any]]]:
    doc_paths = {repo_root / d["path"] for d in docs}
    doc_by_path = {repo_root / d["path"]: d for d in docs}
    deps: dict[Path, list[Path]] = {}
    for d in docs:
        path = repo_root / d["path"]
        deps[path] = [repo_root / rd for rd in d["related_docs"] if (repo_root / rd) in doc_paths]
    assigned: dict[Path, int] = {}

    def get_level(doc: Path, visiting: set[Path]) -> int:
        if doc in assigned:
            return assigned[doc]
        if doc in visiting:
            return 0
        if not deps.get(doc):
            assigned[doc] = 0
            return 0
        visiting.add(doc)
        max_dep = max((get_level(dep, visiting) for dep in deps[doc]), default=-1)
        visiting.remove(doc)
        level = max_dep + 1
        assigned[doc] = level
        return level

    for path in doc_paths:
        get_level(path, set())
    max_level = max(assigned.values()) if assigned else 0
    levels: list[list[dict[str, Any]]] = [[] for _ in range(max_level + 1)]
    for path, level in assigned.items():
        levels[level].append(doc_by_path[path])
    return [level for level in levels if level]


def _print_default(result: AffectedResult) -> None:
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


def _rel_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _print_verbose(result: AffectedResult, changed_files: list[str], repo_root: Path) -> None:
    print(f"Changed files ({len(changed_files)}):")
    for f in changed_files:
        print(f"  {f}")

    print(f"\nMatched ({len(result.matches)} sources -> {len(result.direct_hits)} docs):")
    for source, docs in sorted(result.matches.items()):
        doc_names = ", ".join(_rel_path(d, repo_root) for d in docs)
        print(f"  {source} -> {doc_names}")

    print(f"\nDirect hits ({len(result.direct_hits)}):")
    for doc in result.direct_hits:
        print(f"  {_rel_path(doc, repo_root)}")

    if result.indirect_hits:
        print(f"\nIndirect hits ({len(result.indirect_hits)}):")
        for doc in result.indirect_hits:
            via = result.indirect_chains.get(doc)
            via_str = f" <- {_rel_path(via, repo_root)}" if via else ""
            print(f"  {_rel_path(doc, repo_root)}{via_str}")

    if result.circular_refs:
        print("\nWarning: circular refs detected:")
        for src, dst in result.circular_refs:
            print(f"  {src} <-> {dst}")


def _print_ordered(levels: list[list[dict[str, Any]]]) -> None:
    for i, level_docs in enumerate(levels):
        if not level_docs:
            continue
        if i == 0:
            print("Phase 1 - Independent:")
        else:
            print(f"\nPhase {i + 1} - Level {i}:")
        for doc in level_docs:
            sources = ", ".join(doc["related_sources"]) if doc["related_sources"] else ""
            if sources:
                print(f"  {doc['path']} (sources: {sources})")
            else:
                print(f"  {doc['path']}")


def run(
    docs_path: Path,
    since_lock: bool = False,
    last: int | None = None,
    base_branch: str | None = None,
    since: str | None = None,
    verbose: bool = False,
    output_ordered: bool = False,
) -> int:
    from docsync.core.config import load_config

    config = load_config()
    repo_root = find_repo_root(docs_path)
    try:
        commit_ref = resolve_commit_ref(repo_root, since_lock, last, base_branch, since)
    except ValueError as e:
        print(f"Scope error: {e}", file=sys.stderr)
        return 2

    changed_files = get_changed_files(commit_ref, repo_root)
    result = _find_affected_docs_for_changes(docs_path, changed_files, config, repo_root)

    if not result.affected_docs:
        if verbose:
            print(f"Changed files ({len(changed_files)}):")
            for f in changed_files:
                print(f"  {f}")
            print("\nNo docs affected")
        else:
            print("No docs affected")
        return 0

    if verbose:
        _print_verbose(result, changed_files, repo_root)
    elif output_ordered:
        docs_metadata = _get_doc_metadata(result.affected_docs, config, repo_root)
        levels = _build_levels(docs_metadata, repo_root)
        _print_ordered(levels)
    else:
        _print_default(result)

    return 0
