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


def run(docs_path: Path) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)
    docs_path = docs_path.resolve()
    tree = build_dependency_tree(docs_path, config, repo_root)

    if tree.circular:
        print("Circular refs:")
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

    errors: list[tuple[Path, RefError]] = []
    for doc_path in tree.index.parsed_cache.keys():
        result = _check_single_doc(doc_path, repo_root, tree.index.parsed_cache[doc_path], config)
        for error in result.errors:
            errors.append((doc_path, error))

    if errors:
        print()
        print(f"Warnings ({len(errors)}):")
        for doc_path, error in errors:
            print(f"  {doc_path.relative_to(repo_root)}:{error.ref.line_number}: {error.message}")
        return 1

    return 0
