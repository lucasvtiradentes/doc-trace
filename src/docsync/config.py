import json
from pathlib import Path
from typing import Any

from docsync.constants import CONFIG_FILENAME, DEFAULT_CONFIG


class Config:
    def __init__(self, data: dict[str, Any]):
        self.ignored_paths: list[str] = data.get("ignored_paths", DEFAULT_CONFIG["ignored_paths"])
        self.cascade_depth_limit: int | None = data.get("cascade_depth_limit", DEFAULT_CONFIG["cascade_depth_limit"])
        validation = data.get("validation", DEFAULT_CONFIG["validation"])
        self.parallel_agents: int = validation.get("parallel_agents", DEFAULT_CONFIG["validation"]["parallel_agents"])
        self.timeout_per_doc: int = validation.get("timeout_per_doc", DEFAULT_CONFIG["validation"]["timeout_per_doc"])


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
        config_path = current / CONFIG_FILENAME
        if config_path.exists():
            return config_path
        current = current.parent
    return None


def init_config(target_dir: Path) -> Path:
    config_path = target_dir / CONFIG_FILENAME
    with open(config_path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    return config_path
