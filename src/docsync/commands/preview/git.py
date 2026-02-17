from __future__ import annotations

import subprocess
from pathlib import Path


def get_file_history(repo_root: Path, file_path: str, limit: int = 20) -> list[dict]:
    try:
        result = subprocess.run(
            ["git", "log", f"-{limit}", "--pretty=format:%H|%h|%s|%ai|%an", "--", file_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []
        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|", 4)
            if len(parts) >= 5:
                commits.append({
                    "hash": parts[0],
                    "short": parts[1],
                    "message": parts[2],
                    "date": parts[3],
                    "author": parts[4],
                })
        return commits
    except Exception:
        return []


def get_file_at_commit(repo_root: Path, file_path: str, commit: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{file_path}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception:
        return None
