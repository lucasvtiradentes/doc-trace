from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from doctrace.core.config import Config, find_repo_root, load_config
from doctrace.core.docs import RefEntry, build_dependency_tree


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


def _build_data(tree, errors: list[tuple[Path, RefError]], repo_root: Path) -> dict[str, Any]:
    phases: dict[str, list[str]] = {}
    for i, level_docs in enumerate(tree.levels):
        if not level_docs:
            continue
        label = "independent" if i == 0 else str(i)
        phases[label] = [str(doc.relative_to(repo_root)) for doc in sorted(level_docs)]

    data: dict[str, Any] = {"phases": phases}

    if tree.circular:
        data["circular_refs"] = [
            [str(a.relative_to(repo_root)), str(b.relative_to(repo_root))] for a, b in tree.circular
        ]

    if errors:
        data["warnings"] = [
            {
                "doc": str(doc_path.relative_to(repo_root)),
                "line": error.ref.line_number,
                "message": error.message,
            }
            for doc_path, error in errors
        ]

    return data


def _print_from_data(data: dict[str, Any]) -> None:
    if data.get("circular_refs"):
        print("Circular refs:")
        for pair in data["circular_refs"]:
            print(f"  {pair[0]} <-> {pair[1]}")
        print()

    for label, docs in data["phases"].items():
        phase_label = "Independent" if label == "independent" else f"Phase {label}"
        print(f"{phase_label} ({len(docs)}):")
        for doc in docs:
            print(f"  {doc}")

    warnings = data.get("warnings", [])
    if warnings:
        print()
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  {w['doc']}:{w['line']}: {w['message']}")


def run(docs_path: Path, output_json: bool = False) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)
    docs_path = docs_path.resolve()
    tree = build_dependency_tree(docs_path, config, repo_root)

    errors: list[tuple[Path, RefError]] = []
    for doc_path in tree.index.parsed_cache.keys():
        result = _check_single_doc(doc_path, repo_root, tree.index.parsed_cache[doc_path], config)
        for error in result.errors:
            errors.append((doc_path, error))

    data = _build_data(tree, errors, repo_root)

    if output_json:
        print(json.dumps(data, indent=2))
    else:
        _print_from_data(data)

    return 1 if data.get("warnings") else 0
