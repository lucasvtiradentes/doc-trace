from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

from doctrace.core.config import Config, find_repo_root, load_config
from doctrace.core.docs import ParsedDoc, RefEntry, build_dependency_tree


@dataclass
class RefError:
    doc_path: Path
    ref: RefEntry
    message: str
    ref_type: str


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
            result.errors.append(RefError(doc_path, ref, f"required doc not found: {ref.path}", "required"))
    for ref in parsed.related_docs:
        ref_path = repo_root / ref.path
        if not ref_path.exists():
            result.errors.append(RefError(doc_path, ref, f"related doc not found: {ref.path}", "related"))
    for ref in parsed.sources:
        ref_path = repo_root / ref.path
        if not ref_path.exists() and not _glob_matches(ref.path, repo_root):
            result.errors.append(RefError(doc_path, ref, f"source not found: {ref.path}", "source"))
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
    levels: dict[str, list[dict[str, Any]]] = {}
    for i, level_docs in enumerate(tree.levels):
        if not level_docs:
            continue
        docs_info = []
        for doc in sorted(level_docs):
            rel_path = str(doc.relative_to(repo_root))
            parsed = tree.index.parsed_cache.get(doc)
            req_count = len(parsed.required_docs) if parsed else 0
            rel_count = len(parsed.related_docs) if parsed else 0
            docs_info.append({"path": rel_path, "required": req_count, "related": rel_count})
        levels[str(i)] = docs_info

    data: dict[str, Any] = {"levels": levels}

    if tree.circular:
        data["circular_refs"] = [
            [str(a.relative_to(repo_root)), str(b.relative_to(repo_root))] for a, b in tree.circular
        ]

    if errors:
        data["missing_refs"] = [
            {
                "doc": str(doc_path.relative_to(repo_root)),
                "ref": error.ref.path,
                "type": error.ref_type,
            }
            for doc_path, error in errors
        ]

    if undeclared_inline:
        data["undeclared_inline_refs"] = [
            {"doc": str(doc.relative_to(repo_root)), "ref": ref} for doc, ref in undeclared_inline
        ]

    total_docs = sum(len(docs) for docs in tree.levels)
    max_level = len(tree.levels) - 1 if tree.levels else 0
    data["summary"] = {
        "total_docs": total_docs,
        "levels": len([lvl for lvl in tree.levels if lvl]),
        "max_level": max_level,
        "circular_count": len(tree.circular),
        "missing_count": len(errors),
        "undeclared_inline_count": len(undeclared_inline),
    }

    return data


def _print_section_header(title: str) -> None:
    print(f"\n## {title}")
    print("-" * 40)


def _print_from_data(data: dict[str, Any]) -> None:
    print("=" * 60)
    print("DOCUMENTATION DEPENDENCY ANALYSIS")
    print("=" * 60)

    _print_section_header("Circular Dependencies (required_docs)")
    circular = data.get("circular_refs", [])
    if circular:
        print("ERROR: Found circular dependencies!")
        for pair in circular:
            print(f"  {pair[0]}")
            print(f"    <-> {pair[1]}")
    else:
        print("OK: No circular dependencies found")

    _print_section_header("Missing Referenced Docs")
    missing = data.get("missing_refs", [])
    if missing:
        print("ERROR: Referenced docs not found!")
        for m in missing:
            print(f"  {m['doc']} -> {m['ref']} ({m['type']})")
    else:
        print("OK: All referenced docs exist")

    _print_section_header("Documentation Levels (by required_docs depth)")
    levels = data.get("levels", {})
    for level_num in sorted(levels.keys(), key=int):
        docs = levels[level_num]
        print(f"\nLevel {level_num}:")
        max_path_len = max((len(d["path"]) for d in docs), default=0)
        for d in docs:
            path = d["path"]
            padding = " " * (max_path_len - len(path) + 2)
            print(f"  {path}{padding}(req: {d['required']}, rel: {d['related']})")

    _print_section_header("Inline Reference Check")
    undeclared = data.get("undeclared_inline_refs", [])
    if undeclared:
        print("ERROR: Inline refs not in related_docs:")
        for u in undeclared:
            print(f"  {u['doc']} -> {u['ref']}")
    else:
        print("OK: All inline refs are in related_docs")

    _print_section_header("Summary")
    s = data["summary"]
    print(f"Total docs: {s['total_docs']}")
    print(f"Levels: {s['levels']} (0 to {s['max_level']})")
    print(f"Circular deps (required): {s['circular_count']}")
    print(f"Missing referenced docs: {s['missing_count']}")
    print(f"Missing inline refs: {s['undeclared_inline_count']}")


def _filter_parsed_cache(
    parsed_cache: dict[Path, ParsedDoc], repo_root: Path, ignore_patterns: list[str]
) -> dict[Path, ParsedDoc]:
    if not ignore_patterns:
        return parsed_cache
    filtered = {}
    for doc_path, parsed in parsed_cache.items():
        rel_path = str(doc_path.relative_to(repo_root))
        if not any(fnmatch.fnmatch(rel_path, pat) for pat in ignore_patterns):
            filtered[doc_path] = parsed
    return filtered


def run(docs_path: Path, output_json: bool = False, ignore_patterns: list[str] | None = None) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)
    docs_path = docs_path.resolve()
    tree = build_dependency_tree(docs_path, config, repo_root)

    all_ignore = config.ignore_inline_refs + (ignore_patterns or [])
    filtered_cache = _filter_parsed_cache(tree.index.parsed_cache, repo_root, all_ignore)

    errors: list[tuple[Path, RefError]] = []
    for doc_path in filtered_cache.keys():
        result = _check_single_doc(doc_path, repo_root, filtered_cache[doc_path], config)
        for error in result.errors:
            errors.append((doc_path, error))

    docs_prefix = str(docs_path.relative_to(repo_root)) + "/"
    undeclared_inline = find_undeclared_inline_refs(filtered_cache, repo_root, docs_prefix, [])

    filtered_levels = []
    for level_docs in tree.levels:
        filtered_level = [doc for doc in level_docs if doc in filtered_cache]
        filtered_levels.append(filtered_level)

    filtered_circular = [(a, b) for a, b in tree.circular if a in filtered_cache and b in filtered_cache]

    filtered_tree = SimpleNamespace(
        levels=filtered_levels,
        circular=filtered_circular,
        index=SimpleNamespace(parsed_cache=filtered_cache),
    )

    data = _build_data(filtered_tree, errors, undeclared_inline, repo_root)

    if output_json:
        print(json.dumps(data, indent=2))
    else:
        _print_from_data(data)

    has_errors = tree.circular or errors or undeclared_inline
    return 1 if has_errors else 0
