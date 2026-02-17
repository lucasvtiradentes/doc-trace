import re

RELATED_DOCS_PATTERN = re.compile(r"^related docs:\s*$", re.MULTILINE | re.IGNORECASE)
RELATED_SOURCES_PATTERN = re.compile(r"^related sources:\s*$", re.MULTILINE | re.IGNORECASE)
LIST_ITEM_PATTERN = re.compile(r"^-\s+(\S+)\s+-\s+(.+)$")

DOCSYNC_DIR = ".docsync"
CONFIG_FILENAME = "config.json"
LOCK_FILENAME = "lock.json"
PROMPT_FILENAME = "prompt.md"

DEFAULT_CONFIG = {
    "ignored_paths": [],
    "cascade_depth_limit": None,
}

DEFAULT_LOCK = {"last_analyzed_commit": None, "last_run": None, "docs_validated": []}

DEFAULT_PROMPT = """Validate {count} docs by launching PARALLEL agents (one per doc).

For each doc, launch a subagent that will:
1. Read the doc file
2. Read all its related sources
3. Check if the doc content accurately describes the source code
4. Report any outdated, incorrect, or missing information

IMPORTANT: Launch ALL agents in a SINGLE message for parallel execution.

Docs to validate:

{docs_list}"""
