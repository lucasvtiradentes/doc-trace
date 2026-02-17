import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from docsync.core.constants import DOCSYNC_DIR, LOCK_FILENAME


class Lock:
    def __init__(self, data: dict[str, Any]):
        self.last_analyzed_commit: str | None = data.get("last_analyzed_commit")
        self.last_run: str | None = data.get("last_run")
        self.docs_validated: list[str] = data.get("docs_validated", [])

    def to_dict(self) -> dict[str, Any]:
        return {
            "last_analyzed_commit": self.last_analyzed_commit,
            "last_run": self.last_run,
            "docs_validated": self.docs_validated,
        }


def load_lock(start_path: Path | None = None) -> Lock:
    lock_path = find_lock(start_path or Path.cwd())
    if lock_path is None:
        return Lock({})
    with open(lock_path) as f:
        data = json.load(f)
    return Lock(data)


def find_lock(start_path: Path) -> Path | None:
    current = start_path.resolve()
    while current != current.parent:
        lock_path = current / DOCSYNC_DIR / LOCK_FILENAME
        if lock_path.exists():
            return lock_path
        current = current.parent
    return None


def save_lock(lock: Lock, repo_root: Path) -> Path:
    docsync_dir = repo_root / DOCSYNC_DIR
    docsync_dir.mkdir(exist_ok=True)
    lock_path = docsync_dir / LOCK_FILENAME
    lock.last_run = datetime.now(timezone.utc).isoformat()
    with open(lock_path, "w") as f:
        json.dump(lock.to_dict(), f, indent=2)
    return lock_path


def get_current_commit() -> str | None:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
