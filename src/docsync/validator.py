import fnmatch
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    docs_path = docs_path.resolve()
    repo_root = _find_repo_root(docs_path)
    doc_files = list(docs_path.rglob("*.md"))
    if incremental:
        from docsync.cascade import find_affected_docs
        from docsync.lock import load_lock

        lock = load_lock(repo_root)
        if lock.last_analyzed_commit:
            result = find_affected_docs(docs_path, lock.last_analyzed_commit, config, repo_root)
            affected_set = set(result.affected_docs)
            doc_files = [f for f in doc_files if f in affected_set]
            yield f"Incremental: {len(doc_files)} docs affected since {lock.last_analyzed_commit[:8]}"
        else:
            yield "No previous commit in lock, validating all docs"
    if not doc_files:
        yield "No docs to validate"
        return
    tasks = []
    for doc_file in doc_files:
        parsed = parse_doc(doc_file)
        sources = [ref.path for ref in parsed.related_sources]
        prompt = _build_validation_prompt(doc_file, sources)
        tasks.append((doc_file, prompt))
    validated = []
    yield f"Validating {len(tasks)} docs with {config.parallel_agents} parallel agents..."
    with ThreadPoolExecutor(max_workers=config.parallel_agents) as executor:
        futures = {
            executor.submit(_run_claude_validation_sync, doc_path, prompt, config.timeout_per_doc): doc_path
            for doc_path, prompt in tasks
        }
        for future in as_completed(futures):
            doc_path = futures[future]
            try:
                output = future.result()
                yield output
                validated.append(str(doc_path.relative_to(repo_root)))
            except Exception as e:
                yield f"[{doc_path}] error: {e}"
    if incremental:
        from docsync.lock import Lock, get_current_commit, save_lock

        current = get_current_commit()
        if current:
            new_lock = Lock(
                {
                    "last_analyzed_commit": current,
                    "docs_validated": validated,
                }
            )
            save_lock(new_lock, repo_root)
            yield f"Updated lock to {current[:8]}"


def _build_validation_prompt(doc_path: Path, sources: list[str]) -> str:
    sources_str = "\n".join(f"- {s}" for s in sources)
    return f"""Validate the documentation in {doc_path}.

Read the doc and its related sources:
{sources_str}

Check if the doc content accurately describes the source code.
Report any outdated or incorrect information."""


def _run_claude_validation_sync(doc_path: Path, prompt: str, timeout: int) -> str:
    try:
        result = subprocess.run(["claude", "--print", prompt], capture_output=True, text=True, timeout=timeout)
        output = []
        if result.stdout:
            output.append(f"[{doc_path}]\n{result.stdout}")
        if result.stderr:
            output.append(f"[{doc_path}] stderr: {result.stderr}")
        return "\n".join(output) if output else f"[{doc_path}] no output"
    except subprocess.TimeoutExpired:
        return f"[{doc_path}] validation timed out after {timeout}s"
    except FileNotFoundError:
        return f"[{doc_path}] claude cli not found"
