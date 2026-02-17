import fnmatch
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from docsync.config import Config
from docsync.parser import RefEntry, parse_doc


@dataclass
class RefError:
    doc_path: Path
    ref: RefEntry
    message: str


@dataclass
class CheckResult:
    doc_path: Path
    errors: list[RefError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def check_refs(docs_path: Path, config: Config, repo_root: Path | None = None) -> Iterator[CheckResult]:
    docs_path = docs_path.resolve()
    if repo_root is None:
        repo_root = _find_repo_root(docs_path)
    doc_files = list(docs_path.rglob("*.md"))
    for doc_file in doc_files:
        if _is_ignored(doc_file, config.ignored_paths, repo_root):
            continue
        yield _check_single_doc(doc_file, repo_root)


def _check_single_doc(doc_path: Path, repo_root: Path) -> CheckResult:
    result = CheckResult(doc_path=doc_path)
    try:
        parsed = parse_doc(doc_path)
    except Exception as e:
        result.errors.append(
            RefError(
                doc_path=doc_path,
                ref=RefEntry(path="", description="", line_number=0),
                message=f"failed to parse doc: {e}",
            )
        )
        return result
    for ref in parsed.related_docs:
        ref_path = repo_root / ref.path
        if not ref_path.exists():
            result.errors.append(RefError(doc_path=doc_path, ref=ref, message=f"related doc not found: {ref.path}"))
    for ref in parsed.related_sources:
        ref_path = repo_root / ref.path
        if not ref_path.exists() and not _glob_matches(ref.path, repo_root):
            result.errors.append(RefError(doc_path=doc_path, ref=ref, message=f"related source not found: {ref.path}"))
    return result


def _glob_matches(pattern: str, repo_root: Path) -> bool:
    if "*" in pattern or "?" in pattern:
        matches = list(repo_root.glob(pattern))
        return len(matches) > 0
    return False


def _is_ignored(path: Path, ignored_patterns: list[str], repo_root: Path) -> bool:
    rel_path = str(path.relative_to(repo_root))
    for pattern in ignored_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def _find_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def generate_validation_report(docs_path: Path, config: Config, incremental: bool = False) -> dict[str, Any]:
    docs_path = docs_path.resolve()
    repo_root = _find_repo_root(docs_path)
    doc_files = list(docs_path.rglob("*.md"))
    metadata: dict[str, Any] = {"incremental": incremental}
    if incremental:
        from docsync.cascade import find_affected_docs
        from docsync.lock import load_lock

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
        parsed = parse_doc(doc_file)
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


def print_validation_report(docs_path: Path, config: Config, incremental: bool = False) -> str:
    report = generate_validation_report(docs_path, config, incremental)
    return json.dumps(report, indent=2)


def generate_validation_prompt(docs_path: Path, config: Config, incremental: bool = False) -> str:
    report = generate_validation_report(docs_path, config, incremental)
    docs = report["docs"]
    if not docs:
        return "No docs to validate."
    lines = [
        f"Validate {len(docs)} docs by launching PARALLEL agents (one per doc).",
        "",
        "For each doc, launch a subagent that will:",
        "1. Read the doc file",
        "2. Read all its related sources",
        "3. Check if the doc content accurately describes the source code",
        "4. Report any outdated, incorrect, or missing information",
        "",
        "IMPORTANT: Launch ALL agents in a SINGLE message for parallel execution.",
        "",
        "Docs to validate:",
        "",
    ]
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
