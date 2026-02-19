from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple

from doctrace.core.config import Config, find_repo_root, load_config
from doctrace.core.docs import ParsedDoc, build_doc_index, compute_levels, parse_doc
from doctrace.core.git import (
    FileChange,
    get_changed_files,
    get_changed_files_detailed,
    get_commits_in_range,
    get_merge_base,
    get_merged_branches_in_range,
    get_tags_in_range,
)


class AffectedResult(NamedTuple):
    affected_docs: list[Path]
    direct_hits: list[Path]
    indirect_hits: list[Path]
    circular_refs: list[tuple[Path, Path]]
    matches: dict[str, list[Path]]
    indirect_chains: dict[Path, Path]
    parsed_cache: dict[Path, ParsedDoc]


def resolve_commit_ref(
    repo_root: Path,
    since_base: bool = False,
    last: int | None = None,
    base_branch: str | None = None,
    since: str | None = None,
) -> str:
    options_selected = int(since_base) + int(last is not None) + int(base_branch is not None) + int(since is not None)
    if options_selected != 1:
        raise ValueError("choose exactly one scope: --since-base, --last <N>, --base-branch <branch>, or --since <ref>")
    if since_base:
        config = load_config(repo_root, validate=False)
        if not config.base.is_set:
            raise ValueError("doctrace.json has no base; run 'doctrace base update' first")
        assert config.base.commit_hash is not None
        return config.base.commit_hash
    if last is not None:
        if last <= 0:
            raise ValueError("--last must be greater than 0")
        return f"HEAD~{last}"
    if base_branch is not None:
        commit = get_merge_base(base_branch, repo_root)
        if not commit:
            raise ValueError(f"could not resolve merge-base with branch '{base_branch}'")
        return commit
    if since is None:
        raise ValueError("since cannot be None")
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
        return AffectedResult([], [], [], [], {}, {}, {})
    index = build_doc_index(docs_path, config, repo_root)
    direct_hits, matches = _find_direct_hits(changed_files, index.source_to_docs)
    indirect_hits, circular_refs, indirect_chains = _propagate(direct_hits, index.reverse_deps)
    all_affected = list(set(direct_hits) | set(indirect_hits))
    return AffectedResult(
        affected_docs=all_affected,
        direct_hits=direct_hits,
        indirect_hits=indirect_hits,
        circular_refs=circular_refs,
        matches=matches,
        indirect_chains=indirect_chains,
        parsed_cache=index.parsed_cache,
    )


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
    initial_docs: list[Path], doc_to_docs: dict[Path, list[Path]]
) -> tuple[list[Path], list[tuple[Path, Path]], dict[Path, Path]]:
    indirect_hits = []
    indirect_chains: dict[Path, Path] = {}
    visited = set(initial_docs)
    current_level = set(initial_docs)
    while current_level:
        next_level = set()
        for doc in current_level:
            for referencing_doc in doc_to_docs.get(doc, []):
                if referencing_doc in visited:
                    continue
                visited.add(referencing_doc)
                indirect_hits.append(referencing_doc)
                indirect_chains[referencing_doc] = doc
                next_level.add(referencing_doc)
        current_level = next_level
    circular_refs = _find_circular_refs(visited, doc_to_docs)
    return indirect_hits, circular_refs, indirect_chains


def _find_circular_refs(affected_docs: set[Path], doc_to_docs: dict[Path, list[Path]]) -> list[tuple[Path, Path]]:
    circular = []
    seen_pairs: set[tuple[Path, Path]] = set()
    for doc_a in affected_docs:
        for doc_b in doc_to_docs.get(doc_a, []):
            if doc_b not in affected_docs:
                continue
            if doc_a in doc_to_docs.get(doc_b, []):
                pair = (min(doc_a, doc_b), max(doc_a, doc_b))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    circular.append((doc_a, doc_b))
    return circular


def _get_doc_metadata(
    docs: list[Path],
    config: Config,
    repo_root: Path,
    parsed_cache: dict[Path, ParsedDoc] | None = None,
) -> list[dict[str, Any]]:
    result = []
    for doc_file in docs:
        try:
            abs_path = doc_file if doc_file.is_absolute() else repo_root / doc_file
            if parsed_cache and abs_path in parsed_cache:
                parsed = parsed_cache[abs_path]
            else:
                parsed = parse_doc(abs_path, config.metadata)
            rel_path = str(abs_path.relative_to(repo_root))
            result.append(
                {
                    "path": rel_path,
                    "required_docs": [ref.path for ref in parsed.required_docs],
                    "related_docs": [ref.path for ref in parsed.related_docs],
                    "sources": [ref.path for ref in parsed.sources],
                }
            )
        except (OSError, UnicodeDecodeError, ValueError):
            continue
    return result


def _build_levels(docs: list[dict[str, Any]], repo_root: Path) -> list[list[dict[str, Any]]]:
    doc_paths = {repo_root / d["path"] for d in docs}
    doc_by_path = {repo_root / d["path"]: d for d in docs}
    deps: dict[Path, list[Path]] = {}
    for d in docs:
        path = repo_root / d["path"]
        deps[path] = [repo_root / rd for rd in d["required_docs"] if (repo_root / rd) in doc_paths]
    level_result = compute_levels(deps)
    return [[doc_by_path[p] for p in level_paths] for level_paths in level_result.levels if level_paths]


def _rel_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _build_output_data(
    result: AffectedResult,
    levels: list[list[dict[str, Any]]],
    repo_root: Path,
    git_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data: dict[str, Any] = {
        "direct_hits": [_rel_path(d, repo_root) for d in result.direct_hits],
        "indirect_hits": [
            {"doc": _rel_path(d, repo_root), "via": _rel_path(result.indirect_chains[d], repo_root)}
            for d in result.indirect_hits
            if d in result.indirect_chains
        ],
        "phases": {str(i + 1): [d["path"] for d in level] for i, level in enumerate(levels)},
    }
    if result.circular_refs:
        data["circular_refs"] = [[_rel_path(a, repo_root), _rel_path(b, repo_root)] for a, b in result.circular_refs]
    if git_data:
        data["git"] = git_data
    return data


def _build_git_data(
    changed_files: list[FileChange],
    result: AffectedResult,
    commit_ref: str,
    repo_root: Path,
) -> dict[str, Any]:
    commits = get_commits_in_range(commit_ref, repo_root)
    tags = get_tags_in_range(commit_ref, repo_root)
    merged_branches = get_merged_branches_in_range(commit_ref, repo_root)
    return {
        "commits": {c.short: c.message for c in commits},
        "tags": tags,
        "merged_branches": merged_branches,
        "changed_files": [
            {
                "path": fc.path,
                "status": fc.status,
                "added": fc.added,
                "removed": fc.removed,
                **({"old_path": fc.old_path} if fc.old_path else {}),
            }
            for fc in changed_files
        ],
        "source_to_docs": {src: [_rel_path(d, repo_root) for d in docs] for src, docs in result.matches.items()},
    }


def _print_from_data(data: dict[str, Any], verbose: bool = False) -> None:
    git = data.get("git", {})
    if verbose and git:
        files = git.get("changed_files", [])
        if files:
            print(f"Changed files ({len(files)}):")
            stats_list = []
            for fc in files:
                added = f"+{fc['added']}" if fc.get("added") else ""
                removed = f"-{fc['removed']}" if fc.get("removed") else ""
                if added and removed:
                    stats_list.append(f"({added} {removed})")
                elif added:
                    stats_list.append(f"({added})")
                elif removed:
                    stats_list.append(f"({removed})")
                else:
                    stats_list.append("")
            max_stats = max((len(s) for s in stats_list), default=0)
            for fc, stats in zip(files, stats_list):
                status = fc["status"][0]
                rename = f" <- {fc['old_path']}" if fc.get("old_path") else ""
                print(f"  {status}  {stats.ljust(max_stats)}  {fc['path']}{rename}")

        commits = git.get("commits", {})
        if commits:
            print(f"\nCommits ({len(commits)}):")
            for short_hash, message in commits.items():
                print(f"  {short_hash} {message}")

        tags = git.get("tags", [])
        if tags:
            print(f"\nTags ({len(tags)}): {', '.join(tags)}")

        merged = git.get("merged_branches", [])
        if merged:
            print(f"\nMerged branches ({len(merged)}):")
            for b in merged:
                print(f"  {b}")

        source_to_docs = git.get("source_to_docs", {})
        if source_to_docs:
            total_docs = len(data["direct_hits"])
            print(f"\nMatched ({len(source_to_docs)} sources -> {total_docs} docs):")
            for source, docs in sorted(source_to_docs.items()):
                print(f"  {source} -> {', '.join(docs)}")

    prefix = "\n" if verbose else ""
    print(f"{prefix}Direct hits ({len(data['direct_hits'])}):")
    for doc in data["direct_hits"]:
        print(f"  {doc}")

    if data["indirect_hits"]:
        print(f"\nIndirect hits ({len(data['indirect_hits'])}):")
        for hit in data["indirect_hits"]:
            print(f"  {hit['doc']} <- {hit['via']}")

    if data.get("circular_refs"):
        print("\nWarning: circular refs detected:")
        for ref in data["circular_refs"]:
            print(f"  {ref[0]} <-> {ref[1]}")

    if data["phases"]:
        print(f"\nPhases ({len(data['phases'])}):")
        for phase_num, docs in data["phases"].items():
            print(f"  {phase_num}. {', '.join(docs)}")


def run(
    docs_path: Path,
    since_base: bool = False,
    last: int | None = None,
    base_branch: str | None = None,
    since: str | None = None,
    verbose: bool = False,
    output_json: bool = False,
) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)
    try:
        commit_ref = resolve_commit_ref(repo_root, since_base, last, base_branch, since)
    except ValueError as e:
        if output_json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Scope error: {e}", file=sys.stderr)
        return 2

    changed_files = get_changed_files(commit_ref, repo_root)
    changed_files_detailed = get_changed_files_detailed(commit_ref, repo_root) if verbose else []
    result = _find_affected_docs_for_changes(docs_path, changed_files, config, repo_root)

    if not result.affected_docs:
        data: dict[str, Any] = {"direct_hits": [], "indirect_hits": [], "phases": {}}
        if verbose:
            git_data = _build_git_data(changed_files_detailed, result, commit_ref, repo_root)
            data["git"] = git_data
        if output_json:
            print(json.dumps(data, indent=2))
        elif verbose:
            _print_from_data(data, verbose=True)
            print("\nNo docs affected")
        else:
            print("No docs affected")
        return 0

    docs_metadata = _get_doc_metadata(result.affected_docs, config, repo_root, result.parsed_cache)
    levels = _build_levels(docs_metadata, repo_root)

    git_data = _build_git_data(changed_files_detailed, result, commit_ref, repo_root) if verbose else None
    data = _build_output_data(result, levels, repo_root, git_data)

    if output_json:
        print(json.dumps(data, indent=2))
    else:
        _print_from_data(data, verbose=verbose)

    return 0
