from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from doctrace.core.config import Config, find_repo_root
from doctrace.core.constants import MARKDOWN_GLOB
from doctrace.core.parser import RefEntry, parse_doc


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
        return len(self.errors) == 0


def validate_refs(docs_path: Path, config: Config, repo_root: Path | None = None) -> Iterator[ValidateResult]:
    docs_path = docs_path.resolve()
    if repo_root is None:
        repo_root = find_repo_root(docs_path)
    doc_files = list(docs_path.rglob(MARKDOWN_GLOB))
    for doc_file in doc_files:
        yield _check_single_doc(doc_file, repo_root, config)


def _check_single_doc(doc_path: Path, repo_root: Path, config: Config) -> ValidateResult:
    result = ValidateResult(doc_path=doc_path)
    try:
        parsed = parse_doc(doc_path, config.metadata)
    except Exception as e:
        result.errors.append(
            RefError(
                doc_path=doc_path,
                ref=RefEntry(path="", description="", line_number=0),
                message=f"failed to parse doc: {e}",
            )
        )
        return result
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
        matches = list(repo_root.glob(pattern))
        return len(matches) > 0
    return False


def run(docs_path: Path) -> int:
    from doctrace.core.config import load_config

    config = load_config()
    has_errors = False
    for result in validate_refs(docs_path, config):
        if not result.ok:
            has_errors = True
            for error in result.errors:
                print(f"{result.doc_path}:{error.ref.line_number}: {error.message}")
    if has_errors:
        return 1
    print("All refs valid")
    return 0
