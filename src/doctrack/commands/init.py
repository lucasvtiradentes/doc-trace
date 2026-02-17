from pathlib import Path

from doctrack.core.config import init_doctrack


def run() -> int:
    doctrack_dir = init_doctrack(Path.cwd())
    print(f"Created {doctrack_dir}/")
    return 0
