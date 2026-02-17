from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from docsync.core.constants import CONFIG_FILENAME, DEFAULT_CONFIG, DEFAULT_METADATA, DOCSYNC_DIR, SYNCS_DIR


class ConfigError(Exception):
    pass


class MetadataConfig:
    def __init__(self, data: dict[str, Any]):
        self.style: str = data.get("style", DEFAULT_METADATA["style"])
        self.docs_key: str = data.get("docs_key", DEFAULT_METADATA["docs_key"])
        self.sources_key: str = data.get("sources_key", DEFAULT_METADATA["sources_key"])
        self.require_separator: bool = data.get("require_separator", DEFAULT_METADATA["require_separator"])


class Config:
    def __init__(self, data: dict[str, Any]):
        self.ignored_paths: list[str] = data.get("ignored_paths", DEFAULT_CONFIG["ignored_paths"])
        self.cascade_depth_limit: int | None = data.get("cascade_depth_limit", DEFAULT_CONFIG["cascade_depth_limit"])
        self.metadata: MetadataConfig = MetadataConfig(data.get("metadata", {}))


def validate_config(data: dict[str, Any], config_path: Path | None = None) -> list[str]:
    errors = []
    valid_keys = {"ignored_paths", "cascade_depth_limit", "metadata"}
    for key in data:
        if key not in valid_keys:
            errors.append(f"unknown key: {key}")
    if "ignored_paths" in data:
        if not isinstance(data["ignored_paths"], list):
            errors.append("ignored_paths must be a list")
        elif not all(isinstance(p, str) for p in data["ignored_paths"]):
            errors.append("ignored_paths must contain only strings")
    if "cascade_depth_limit" in data:
        val = data["cascade_depth_limit"]
        if val is not None and not isinstance(val, int):
            errors.append("cascade_depth_limit must be null or integer")
    if "metadata" in data:
        errors.extend(_validate_metadata(data["metadata"]))
    return errors


def _validate_metadata(data: Any) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["metadata must be an object"]
    valid_keys = {"style", "docs_key", "sources_key", "require_separator"}
    for key in data:
        if key not in valid_keys:
            errors.append(f"metadata: unknown key: {key}")
    if "style" in data:
        if data["style"] not in ("frontmatter", "custom"):
            errors.append("metadata.style must be 'frontmatter' or 'custom'")
    if "docs_key" in data and not isinstance(data["docs_key"], str):
        errors.append("metadata.docs_key must be a string")
    if "sources_key" in data and not isinstance(data["sources_key"], str):
        errors.append("metadata.sources_key must be a string")
    if "require_separator" in data and not isinstance(data["require_separator"], bool):
        errors.append("metadata.require_separator must be a boolean")
    return errors


def load_config(start_path: Path | None = None, validate: bool = True) -> Config:
    config_path = find_config(start_path or Path.cwd())
    if config_path is None:
        return Config({})
    with open(config_path) as f:
        data = json.load(f)
    if validate:
        errors = validate_config(data, config_path)
        if errors:
            raise ConfigError(f"{config_path}: {', '.join(errors)}")
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
