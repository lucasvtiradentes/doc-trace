from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from doctrace.core.config import Config, find_repo_root, load_config
from doctrace.core.docs import build_dependency_tree
from doctrace.core.parser import RefEntry


@dataclass
class RefError:
    doc_path: Path
    ref: RefEntry
    message: str


@dataclass
class ValidateResult:
    doc_path: Path
    errors: list[RefError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_refs(docs_path: Path, config: Config, repo_root: Path) -> Iterator[ValidateResult]:
    docs_path = docs_path.resolve()
    tree = build_dependency_tree(docs_path, config, repo_root)
    for doc_path in tree.index.parsed_cache.keys():
        yield _check_single_doc(doc_path, repo_root, tree.index.parsed_cache[doc_path], config)


def _check_single_doc(doc_path: Path, repo_root: Path, parsed, config: Config) -> ValidateResult:
    result = ValidateResult(doc_path=doc_path)
    for ref in parsed.required_docs:
        ref_path = repo_root / ref.path
        if not ref_path.exists():
            result.errors.append(RefError(doc_path=doc_path, ref=ref, message=f"required doc not found: {ref.path}"))
    for ref in parsed.related_docs:
        ref_path = repo_root / ref.path
        if not ref_path.exists():
            result.errors.append(RefError(doc_path=doc_path, ref=ref, message=f"related doc not found: {ref.path}"))
    for ref in parsed.sources:
        ref_path = repo_root / ref.path
        if not ref_path.exists() and not _glob_matches(ref.path, repo_root):
            result.errors.append(RefError(doc_path=doc_path, ref=ref, message=f"source not found: {ref.path}"))
    return result


def _glob_matches(pattern: str, repo_root: Path) -> bool:
    if "*" in pattern or "?" in pattern:
        return any(repo_root.glob(pattern))
    return False


def _print_phases(docs_path: Path, config: Config, repo_root: Path) -> None:
    tree = build_dependency_tree(docs_path, config, repo_root)
    if tree.circular:
        print("Warning: circular refs detected:")
        for a, b in tree.circular:
            print(f"  {a.relative_to(repo_root)} <-> {b.relative_to(repo_root)}")
        print()
    for i, level_docs in enumerate(tree.levels):
        if not level_docs:
            continue
        label = "Independent" if i == 0 else f"Phase {i}"
        print(f"{label} ({len(level_docs)}):")
        for doc in sorted(level_docs):
            print(f"  {doc.relative_to(repo_root)}")


def run(docs_path: Path, show_phases: bool = False) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)

    if show_phases:
        _print_phases(docs_path, config, repo_root)
        return 0

    has_errors = False
    for result in validate_refs(docs_path, config, repo_root):
        if not result.ok:
            has_errors = True
            for error in result.errors:
                print(f"{result.doc_path}:{error.ref.line_number}: {error.message}")
    if has_errors:
        return 1
    print("All refs valid")
    return 0
