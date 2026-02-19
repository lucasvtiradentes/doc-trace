DOCSYNC_DIR = ".doctrace"
CONFIG_FILENAME = "config.json"
LOCK_FILENAME = "lock.json"
SYNCS_DIR = "syncs"

DEFAULT_METADATA = {
    "required_docs_key": "required_docs",
    "related_docs_key": "related_docs",
    "sources_key": "sources",
}

DEFAULT_CONFIG = {
    "ignored_paths": [],
    "affected_depth_limit": None,
    "metadata": DEFAULT_METADATA,
}

DEFAULT_LOCK = {"last_analyzed_commit": None, "last_run": None, "docs_validated": []}
