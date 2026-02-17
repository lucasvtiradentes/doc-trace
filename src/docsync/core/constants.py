import re
from pathlib import Path

RELATED_DOCS_PATTERN = re.compile(r"^related docs:\s*$", re.MULTILINE | re.IGNORECASE)
RELATED_SOURCES_PATTERN = re.compile(r"^related sources:\s*$", re.MULTILINE | re.IGNORECASE)
LIST_ITEM_PATTERN = re.compile(r"^-\s+(\S+)\s+-\s+(.+)$")

DOCSYNC_DIR = ".docsync"
CONFIG_FILENAME = "config.json"
LOCK_FILENAME = "lock.json"
SYNC_FILENAME = "sync.md"
SYNCS_DIR = "syncs"

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

DEFAULT_CONFIG = {
    "ignored_paths": [],
    "cascade_depth_limit": None,
}

DEFAULT_LOCK = {"last_analyzed_commit": None, "last_run": None, "docs_validated": []}


def load_default_prompt(parallel: bool = False) -> str:
    filename = "sync-parallel.md" if parallel else "sync.md"
    return (PROMPTS_DIR / filename).read_text()
