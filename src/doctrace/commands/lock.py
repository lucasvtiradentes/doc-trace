from __future__ import annotations

from pathlib import Path

from doctrace.core.config import find_repo_root
from doctrace.core.lock import Lock, get_current_commit, load_lock, save_lock


def run_update(path: Path | None = None) -> int:
    if path is None:
        path = Path.cwd()
    repo_root = find_repo_root(path)
    commit = get_current_commit()
    if not commit:
        print("Could not get current commit")
        return 1
    lock = Lock({"last_analyzed_commit": commit})
    lock_path = save_lock(lock, repo_root)
    print(f"Updated {lock_path}")
    print(f"  last_analyzed_commit: {commit[:12]}")
    return 0


def run_show(path: Path | None = None) -> int:
    if path is None:
        path = Path.cwd()
    lock = load_lock(path)
    if not lock.last_analyzed_commit and not lock.last_run:
        print("No lock file found or lock is empty")
        return 0
    print("Lock state:")
    if lock.last_analyzed_commit:
        print(f"  last_analyzed_commit: {lock.last_analyzed_commit[:12]}")
    else:
        print("  last_analyzed_commit: (not set)")
    if lock.last_run:
        print(f"  last_run: {lock.last_run}")
    else:
        print("  last_run: (not set)")
    return 0
