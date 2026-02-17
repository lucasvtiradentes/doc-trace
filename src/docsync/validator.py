import fnmatch
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

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


def validate_docs(docs_path: Path, config: Config, incremental: bool = False) -> Iterator[str]:
    doc_files = list(docs_path.rglob("*.md"))
    for doc_file in doc_files:
        parsed = parse_doc(doc_file)
        sources = [ref.path for ref in parsed.related_sources]
        prompt = _build_validation_prompt(doc_file, sources)
        yield from _run_claude_validation(doc_file, prompt, config.timeout_per_doc)


def _build_validation_prompt(doc_path: Path, sources: list[str]) -> str:
    sources_str = "\n".join(f"- {s}" for s in sources)
    return f"""Validate the documentation in {doc_path}.

Read the doc and its related sources:
{sources_str}

Check if the doc content accurately describes the source code.
Report any outdated or incorrect information."""


def _run_claude_validation(doc_path: Path, prompt: str, timeout: int) -> Iterator[str]:
    try:
        result = subprocess.run(["claude", "--print", prompt], capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            yield f"[{doc_path}]\n{result.stdout}"
        if result.stderr:
            yield f"[{doc_path}] stderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        yield f"[{doc_path}] validation timed out after {timeout}s"
    except FileNotFoundError:
        yield f"[{doc_path}] claude cli not found"
