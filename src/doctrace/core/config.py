from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from doctrace.core.constants import CONFIG_FILENAME, DEFAULT_METADATA, GIT_DIR
from doctrace.core.git import get_current_commit_info


class ConfigError(Exception):
    pass


class MetadataConfig:
    def __init__(self, data: dict[str, Any]):
        self.required_docs_key: str = data.get("required_docs_key", DEFAULT_METADATA["required_docs_key"])
        self.related_docs_key: str = data.get("related_docs_key", DEFAULT_METADATA["related_docs_key"])
        self.sources_key: str = data.get("sources_key", DEFAULT_METADATA["sources_key"])


class Base:
    def __init__(self, data: dict[str, Any] | None):
        if data is None:
            data = {}
        self.commit_hash: str | None = data.get("commit_hash")
        self.commit_message: str | None = data.get("commit_message")
        self.commit_date: str | None = data.get("commit_date")
        self.analyzed_at: str | None = data.get("analyzed_at")

    def to_dict(self) -> dict[str, Any]:
        return {
            "commit_hash": self.commit_hash,
            "commit_message": self.commit_message,
            "commit_date": self.commit_date,
            "analyzed_at": self.analyzed_at,
        }

    @property
    def is_set(self) -> bool:
        return self.commit_hash is not None


class Config:
    def __init__(self, data: dict[str, Any]):
        self.metadata: MetadataConfig = MetadataConfig(data.get("metadata", {}))
        self.base: Base = Base(data.get("base"))

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self._has_custom_metadata():
            result["metadata"] = {
                "required_docs_key": self.metadata.required_docs_key,
                "related_docs_key": self.metadata.related_docs_key,
                "sources_key": self.metadata.sources_key,
            }
        if self.base.is_set:
            result["base"] = self.base.to_dict()
        return result

    def _has_custom_metadata(self) -> bool:
        return (
            self.metadata.required_docs_key != DEFAULT_METADATA["required_docs_key"]
            or self.metadata.related_docs_key != DEFAULT_METADATA["related_docs_key"]
            or self.metadata.sources_key != DEFAULT_METADATA["sources_key"]
        )


def validate_config(data: dict[str, Any]) -> list[str]:
    errors = []
    valid_keys = {"metadata", "base"}
    for key in data:
        if key not in valid_keys:
            errors.append(f"unknown key: {key}")
    if "metadata" in data:
        errors.extend(_validate_metadata(data["metadata"]))
    return errors


def _validate_metadata(data: Any) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["metadata must be an object"]
    valid_keys = {"required_docs_key", "related_docs_key", "sources_key"}
    for key in data:
        if key not in valid_keys:
            errors.append(f"metadata: unknown key: {key}")
    if "required_docs_key" in data and not isinstance(data["required_docs_key"], str):
        errors.append("metadata.required_docs_key must be a string")
    if "related_docs_key" in data and not isinstance(data["related_docs_key"], str):
        errors.append("metadata.related_docs_key must be a string")
    if "sources_key" in data and not isinstance(data["sources_key"], str):
        errors.append("metadata.sources_key must be a string")
    return errors


def load_config(start_path: Path | None = None, validate: bool = True) -> Config:
    config_path = find_config(start_path or Path.cwd())
    if config_path is None:
        return Config({})
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    if validate:
        errors = validate_config(data)
        if errors:
            raise ConfigError(f"{config_path}: {', '.join(errors)}")
    return Config(data)


def find_config(start_path: Path) -> Path | None:
    current = start_path.resolve()
    while current != current.parent:
        config_path = current / CONFIG_FILENAME
        if config_path.exists():
            return config_path
        current = current.parent
    return None


def find_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    while current != current.parent:
        if (current / GIT_DIR).exists():
            return current
        current = current.parent
    return start_path.resolve()


def save_config(config: Config, repo_root: Path) -> Path:
    config_path = repo_root / CONFIG_FILENAME
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, indent=2)
    return config_path


def update_base(repo_root: Path) -> tuple[Path, Base]:
    config = load_config(repo_root, validate=False)
    commit_info = get_current_commit_info(repo_root)
    if commit_info is None:
        raise ConfigError("Could not get current commit info")
    config.base = Base(
        {
            "commit_hash": commit_info.hash,
            "commit_message": commit_info.message,
            "commit_date": commit_info.date,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    config_path = save_config(config, repo_root)
    return config_path, config.base


def init_config(target_dir: Path) -> Path:
    config_path = target_dir / CONFIG_FILENAME
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)
    return config_path
