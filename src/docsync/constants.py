import re

RELATED_DOCS_PATTERN = re.compile(r"^related docs:\s*$", re.MULTILINE | re.IGNORECASE)
RELATED_SOURCES_PATTERN = re.compile(r"^related sources:\s*$", re.MULTILINE | re.IGNORECASE)
LIST_ITEM_PATTERN = re.compile(r"^-\s+(\S+)\s+-\s+(.+)$")

DEFAULT_CONFIG = {
    "ignored_paths": [],
    "cascade_depth_limit": None,
    "validation": {"parallel_agents": 3, "timeout_per_doc": 120},
}

DEFAULT_LOCK = {"last_analyzed_commit": None, "last_run": None, "docs_validated": []}

CONFIG_FILENAME = ".docsync.json"
LOCK_FILENAME = ".docsync.lock"
