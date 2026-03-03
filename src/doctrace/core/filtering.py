from __future__ import annotations

import fnmatch
from pathlib import Path


def matches_ignore_pattern(path: Path, repo_root: Path, patterns: list[str]) -> bool:
    if not patterns:
        return False
    rel_path = str(path.relative_to(repo_root))
    return any(fnmatch.fnmatch(rel_path, pat) for pat in patterns)
