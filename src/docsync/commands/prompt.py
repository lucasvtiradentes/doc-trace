from __future__ import annotations

import fnmatch
from datetime import datetime
from pathlib import Path
from typing import Any

from docsync.core.config import Config, find_repo_root
from docsync.core.constants import DOCSYNC_DIR, PROMPT_FILENAME, SYNCS_DIR, load_default_prompt
from docsync.core.parser import parse_doc


def generate_validation_report(docs_path: Path, config: Config, incremental: bool = False) -> dict[str, Any]:
    docs_path = docs_path.resolve()
    repo_root = find_repo_root(docs_path)
    doc_files = list(docs_path.rglob("*.md"))
    metadata: dict[str, Any] = {"incremental": incremental}
    if incremental:
        from docsync.commands.affected import find_affected_docs
        from docsync.core.lock import load_lock

        lock = load_lock(repo_root)
        if lock.last_analyzed_commit:
            result = find_affected_docs(docs_path, lock.last_analyzed_commit, config, repo_root)
            affected_set = set(result.affected_docs)
            doc_files = [f for f in doc_files if f in affected_set]
            metadata["since_commit"] = lock.last_analyzed_commit
        else:
            metadata["since_commit"] = None
    docs = []
    for doc_file in doc_files:
        if _is_ignored(doc_file, config.ignored_paths, repo_root):
            continue
        parsed = parse_doc(doc_file, config.metadata)
        rel_path = str(doc_file.relative_to(repo_root))
        docs.append(
            {
                "path": rel_path,
                "related_docs": [ref.path for ref in parsed.related_docs],
                "related_sources": [ref.path for ref in parsed.related_sources],
            }
        )
    return {
        "repo_root": str(repo_root),
        "metadata": metadata,
        "docs": docs,
    }


def _is_ignored(path: Path, ignored_patterns: list[str], repo_root: Path) -> bool:
    rel_path = str(path.relative_to(repo_root))
    for pattern in ignored_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def _load_prompt_template(repo_root: Path) -> str:
    prompt_path = repo_root / DOCSYNC_DIR / PROMPT_FILENAME
    if prompt_path.exists():
        return prompt_path.read_text()
    return load_default_prompt()


def _format_docs_list(docs: list[dict[str, Any]]) -> str:
    lines = []
    for i, doc in enumerate(docs, 1):
        lines.append(f"{i}. {doc['path']}")
        if doc["related_sources"]:
            sources = ", ".join(doc["related_sources"])
            lines.append(f"   sources: {sources}")
        if doc["related_docs"]:
            related = ", ".join(doc["related_docs"])
            lines.append(f"   related docs: {related}")
        lines.append("")
    return "\n".join(lines)


def _format_phases(levels: list[list[dict[str, Any]]]) -> str:
    lines = []
    for i, level_docs in enumerate(levels):
        if not level_docs:
            continue
        if i == 0:
            lines.append("Phase 1 - Independent (launch parallel):")
        else:
            lines.append(f"\nPhase {i + 1} - Level {i} (after phase {i} completes):")
        for doc in level_docs:
            lines.append(f"  {doc['path']}")
            if doc["related_sources"]:
                sources = ", ".join(doc["related_sources"])
                lines.append(f"    sources: {sources}")
        lines.append("")
    return "\n".join(lines)


def _get_syncs_dir() -> str:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    return f".docsync/{SYNCS_DIR}/{timestamp}"


def _build_sync_levels(docs: list[dict[str, Any]], repo_root: Path) -> list[list[dict[str, Any]]]:
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


def generate_prompt(docs_path: Path, config: Config, incremental: bool = False, parallel: bool = False) -> str:
    report = generate_validation_report(docs_path, config, incremental)
    docs = report["docs"]
    if not docs:
        return "No docs found."
    repo_root = Path(report["repo_root"])
    syncs_dir = _get_syncs_dir()
    template = _load_prompt_template(repo_root)

    if parallel:
        docs_formatted = _format_docs_list(docs)
    else:
        levels = _build_sync_levels(docs, repo_root)
        docs_formatted = _format_phases(levels)
    return template.format(count=len(docs), docs=docs_formatted, syncs_dir=syncs_dir)


def run(docs_path: Path, incremental: bool, parallel: bool, update_lock: bool = False) -> int:
    from docsync.core.config import find_repo_root, load_config
    from docsync.core.lock import Lock, get_current_commit, save_lock

    config = load_config()
    print(generate_prompt(docs_path, config, incremental, parallel))
    if update_lock:
        repo_root = find_repo_root(docs_path)
        commit = get_current_commit()
        if commit:
            lock = Lock({"last_analyzed_commit": commit})
            save_lock(lock, repo_root)
    return 0
