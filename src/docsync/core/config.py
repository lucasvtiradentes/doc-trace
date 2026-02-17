import json
from pathlib import Path
from typing import Any

from docsync.core.constants import CONFIG_FILENAME, DEFAULT_CONFIG, DOCSYNC_DIR, SYNCS_DIR


class Config:
    def __init__(self, data: dict[str, Any]):
        self.ignored_paths: list[str] = data.get("ignored_paths", DEFAULT_CONFIG["ignored_paths"])
        self.cascade_depth_limit: int | None = data.get("cascade_depth_limit", DEFAULT_CONFIG["cascade_depth_limit"])


def load_config(start_path: Path | None = None) -> Config:
    config_path = find_config(start_path or Path.cwd())
    if config_path is None:
        return Config({})
    with open(config_path) as f:
        data = json.load(f)
    return Config(data)


def find_config(start_path: Path) -> Path | None:
    current = start_path.resolve()
    while current != current.parent:
        config_path = current / DOCSYNC_DIR / CONFIG_FILENAME
        if config_path.exists():
            return config_path
        current = current.parent
    return None


def find_docsync_dir(start_path: Path) -> Path | None:
    current = start_path.resolve()
    while current != current.parent:
        docsync_dir = current / DOCSYNC_DIR
        if docsync_dir.exists():
            return docsync_dir
        current = current.parent
    return None


def find_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path.resolve()


def init_docsync(target_dir: Path) -> Path:
    docsync_dir = target_dir / DOCSYNC_DIR
    docsync_dir.mkdir(exist_ok=True)
    config_path = docsync_dir / CONFIG_FILENAME
    with open(config_path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    syncs_dir = docsync_dir / SYNCS_DIR
    syncs_dir.mkdir(exist_ok=True)
    gitignore_path = syncs_dir / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write("*\n!.gitignore\n")
    return docsync_dir
