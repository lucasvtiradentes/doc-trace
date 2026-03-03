from __future__ import annotations

import fnmatch
import json
import re
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


def extract_inline_refs(filepath: Path, pattern: re.Pattern[str]) -> list[str]:
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        body_start = 0
    else:
        body_start = 1
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                body_start = i + 1
                break
    body_lines = lines[body_start:]
    in_code_block = False
    filtered = []
    for line in body_lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            line = re.sub(r"`[^`]+`", "", line)
            filtered.append(line)
    body = "\n".join(filtered)
    return list(set(pattern.findall(body)))


def find_undeclared_inline_refs(
    parsed_cache: dict[Path, ParsedDoc], repo_root: Path, docs_prefix: str, ignore_patterns: list[str]
) -> list[tuple[Path, str]]:
    escaped_prefix = re.escape(docs_prefix)
    pattern = re.compile(rf"{escaped_prefix}[a-zA-Z0-9/_.-]+\.md")
    undeclared = []
    for doc_path, parsed in parsed_cache.items():
        if ignore_patterns:
            rel_path = str(doc_path.relative_to(repo_root))
            if any(fnmatch.fnmatch(rel_path, pat) for pat in ignore_patterns):
                continue
        declared = {ref.path for ref in parsed.related_docs}
        declared.update(ref.path for ref in parsed.required_docs)
        inline_refs = extract_inline_refs(doc_path, pattern)
        for ref in inline_refs:
            if ref not in declared:
                undeclared.append((doc_path, ref))
    return undeclared


def _build_data(
    tree,
    errors: list[tuple[Path, RefError]],
    undeclared_inline: list[tuple[Path, str]],
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

    if undeclared_inline:
        data["undeclared_inline_refs"] = [
            {"doc": str(doc.relative_to(repo_root)), "ref": ref} for doc, ref in undeclared_inline
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

    undeclared = data.get("undeclared_inline_refs", [])
    if undeclared:
        print()
        print(f"Undeclared inline refs ({len(undeclared)}):")
        for u in undeclared:
            print(f"  {u['doc']}: {u['ref']} (add to related_docs)")


def run(docs_path: Path, output_json: bool = False, ignore_patterns: list[str] | None = None) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)
    docs_path = docs_path.resolve()
    tree = build_dependency_tree(docs_path, config, repo_root)

    errors: list[tuple[Path, RefError]] = []
    for doc_path in tree.index.parsed_cache.keys():
        result = _check_single_doc(doc_path, repo_root, tree.index.parsed_cache[doc_path], config)
        for error in result.errors:
            errors.append((doc_path, error))

    all_ignore = config.ignore_inline_refs + (ignore_patterns or [])
    docs_prefix = str(docs_path.relative_to(repo_root)) + "/"
    undeclared_inline = find_undeclared_inline_refs(tree.index.parsed_cache, repo_root, docs_prefix, all_ignore)
    data = _build_data(tree, errors, undeclared_inline, repo_root)

    if output_json:
        print(json.dumps(data, indent=2))
    else:
        _print_from_data(data)

    has_issues = data.get("warnings") or data.get("undeclared_inline_refs")
    return 1 if has_issues else 0
