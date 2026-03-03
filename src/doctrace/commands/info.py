from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from doctrace.core.config import Config, find_repo_root, load_config
from doctrace.core.docs import ParsedDoc, RefEntry, build_dependency_tree


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


def find_missing_bidirectional(parsed_cache: dict[Path, ParsedDoc], repo_root: Path) -> list[tuple[Path, Path]]:
    missing = []
    repo_root = repo_root.resolve()
    for doc_a, parsed_a in parsed_cache.items():
        rel_a = str(doc_a.relative_to(repo_root))
        for ref in parsed_a.related_docs:
            doc_b = (repo_root / ref.path).resolve()
            if doc_b not in parsed_cache:
                continue
            parsed_b = parsed_cache[doc_b]
            b_related_paths = {r.path for r in parsed_b.related_docs}
            if rel_a not in b_related_paths:
                missing.append((doc_a, doc_b))
    return missing


def _build_data(
    tree,
    errors: list[tuple[Path, RefError]],
    missing_bidirectional: list[tuple[Path, Path]],
    repo_root: Path,
) -> dict[str, Any]:
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

    if missing_bidirectional:
        data["missing_bidirectional"] = [
            {"doc": str(a.relative_to(repo_root)), "missing_in": str(b.relative_to(repo_root))}
            for a, b in missing_bidirectional
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

    missing_bidir = data.get("missing_bidirectional", [])
    if missing_bidir:
        print()
        print(f"Missing bidirectional refs ({len(missing_bidir)}):")
        for m in missing_bidir:
            print(f"  {m['doc']} -> {m['missing_in']} (should reference back)")


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

    missing_bidirectional = find_missing_bidirectional(tree.index.parsed_cache, repo_root)
    data = _build_data(tree, errors, missing_bidirectional, repo_root)

    if output_json:
        print(json.dumps(data, indent=2))
    else:
        _print_from_data(data)

    has_issues = data.get("warnings") or data.get("missing_bidirectional")
    return 1 if has_issues else 0
