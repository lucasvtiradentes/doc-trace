from __future__ import annotations

import subprocess
from pathlib import Path
from typing import NamedTuple


class FileChange(NamedTuple):
    path: str
    status: str
    added: int | None
    removed: int | None
    old_path: str | None = None


class CurrentCommitInfo(NamedTuple):
    hash: str
    message: str
    date: str


def get_current_commit(cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_current_commit_info(cwd: Path | None = None) -> CurrentCommitInfo | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%H%x00%s%x00%aI"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )
        parts = result.stdout.strip().split("\x00", 2)
        if len(parts) >= 3:
            return CurrentCommitInfo(hash=parts[0], message=parts[1], date=parts[2])
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_merge_base(branch: str, repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "merge-base", "HEAD", branch],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root,
        )
        commit = result.stdout.strip()
        return commit if commit else None
    except subprocess.CalledProcessError:
        return None


def get_changed_files(commit_ref: str, repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", commit_ref],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root,
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def get_changed_files_detailed(commit_ref: str, repo_root: Path) -> list[FileChange]:
    status_map: dict[str, tuple[str, str | None]] = {}
    try:
        result = subprocess.run(
            ["git", "diff", "--name-status", commit_ref],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root,
        )
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            status = parts[0][0]
            if status == "R" and len(parts) >= 3:
                old_path, new_path = parts[1], parts[2]
                status_map[new_path] = (status, old_path)
            elif len(parts) >= 2:
                status_map[parts[1]] = (status, None)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    stats_map: dict[str, tuple[int | None, int | None]] = {}
    try:
        result = subprocess.run(
            ["git", "diff", "--numstat", commit_ref],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root,
        )
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                added = int(parts[0]) if parts[0] != "-" else None
                removed = int(parts[1]) if parts[1] != "-" else None
                path = parts[2]
                if " => " in path:
                    path = path.split(" => ")[-1].rstrip("}")
                    if "{" in parts[2]:
                        prefix = parts[2].split("{")[0]
                        path = prefix + path
                stats_map[path] = (added, removed)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    changes = []
    for path, (status, old_path) in status_map.items():
        added, removed = stats_map.get(path, (None, None))
        changes.append(FileChange(path, status, added, removed, old_path))
    return changes


def get_file_history(repo_root: Path, file_path: str, limit: int = 20) -> list[dict]:
    try:
        result = subprocess.run(
            ["git", "log", f"-{limit}", "--pretty=format:%H%x00%h%x00%s%x00%ai%x00%an", "--", file_path],
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
            parts = line.split("\x00", 4)
            if len(parts) >= 5:
                commits.append(
                    {
                        "hash": parts[0],
                        "short": parts[1],
                        "message": parts[2],
                        "date": parts[3],
                        "author": parts[4],
                    }
                )
        return commits
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
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
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return None


class CommitInfo(NamedTuple):
    hash: str
    short: str
    message: str


def get_commits_in_range(commit_ref: str, repo_root: Path) -> list[CommitInfo]:
    try:
        result = subprocess.run(
            ["git", "log", f"{commit_ref}..HEAD", "--pretty=format:%H%x00%h%x00%s"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        commits = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            parts = line.split("\x00", 2)
            if len(parts) >= 3:
                commits.append(CommitInfo(parts[0], parts[1], parts[2]))
        return commits
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def get_tags_in_range(commit_ref: str, repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "log", f"{commit_ref}..HEAD", "--pretty=format:%D"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        tags = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            for ref in line.split(", "):
                if ref.startswith("tag: "):
                    tags.append(ref[5:])
        return tags
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def get_merged_branches_in_range(commit_ref: str, repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "log", f"{commit_ref}..HEAD", "--merges", "--pretty=format:%s"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        branches = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            if "Merge branch '" in line:
                start = line.find("'") + 1
                end = line.find("'", start)
                if start > 0 and end > start:
                    branches.append(line[start:end])
            elif "Merge pull request" in line:
                branches.append(line)
        return branches
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
