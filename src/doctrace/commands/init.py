from pathlib import Path

from doctrace.core.config import init_config


def run() -> int:
    config_path = init_config(Path.cwd())
    print(f"Created {config_path}")
    return 0
