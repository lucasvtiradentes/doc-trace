from pathlib import Path

from docsync.core.config import init_docsync


def run() -> int:
    docsync_dir = init_docsync(Path.cwd())
    print(f"Created {docsync_dir}/")
    return 0
