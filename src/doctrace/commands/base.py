from __future__ import annotations

from pathlib import Path

from doctrace.core.config import ConfigError, find_repo_root, load_config, update_base


def run_update(path: Path | None = None) -> int:
    if path is None:
        path = Path.cwd()
    repo_root = find_repo_root(path)
    try:
        config_path, base = update_base(repo_root)
    except ConfigError as e:
        print(str(e))
        return 1
    print(f"Updated {config_path}")
    print(f"  commit: {base.commit_hash[:12]} {base.commit_message}")
    return 0


def run_show(path: Path | None = None) -> int:
    if path is None:
        path = Path.cwd()
    config = load_config(path, validate=False)
    if not config.base.is_set:
        print("No base found in doctrace.json")
        return 0
    b = config.base
    print("Base:")
    print(f"  commit_hash:    {b.commit_hash[:12] if b.commit_hash else '(not set)'}")
    print(f"  commit_message: {b.commit_message or '(not set)'}")
    print(f"  commit_date:    {b.commit_date or '(not set)'}")
    print(f"  analyzed_at:    {b.analyzed_at or '(not set)'}")
    return 0
