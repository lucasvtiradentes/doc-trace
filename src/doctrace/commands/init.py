from pathlib import Path

from doctrace.core.config import init_doctrace


def run() -> int:
    doctrace_dir = init_doctrace(Path.cwd())
    print(f"Created {doctrace_dir}/")
    return 0
