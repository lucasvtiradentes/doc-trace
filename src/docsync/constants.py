import re

RELATED_DOCS_PATTERN = re.compile(r"^related docs:\s*$", re.MULTILINE | re.IGNORECASE)
RELATED_SOURCES_PATTERN = re.compile(r"^related sources:\s*$", re.MULTILINE | re.IGNORECASE)
LIST_ITEM_PATTERN = re.compile(r"^-\s+(\S+)\s+-\s+(.+)$")

DOCSYNC_DIR = ".docsync"
CONFIG_FILENAME = "config.json"
LOCK_FILENAME = "lock.json"
SYNC_FILENAME = "sync.md"
SYNCS_DIR = "syncs"

DEFAULT_CONFIG = {
    "ignored_paths": [],
    "cascade_depth_limit": None,
}

DEFAULT_LOCK = {"last_analyzed_commit": None, "last_run": None, "docs_validated": []}

DEFAULT_SYNC_PROMPT = """Sync {count} docs by launching agents in phases (respecting dependencies).

Each agent will:
1. Read the doc + all related sources
2. Fix any outdated/incorrect content directly in the doc
3. Write a report to {syncs_dir}

Report format ({syncs_dir}/{{doc-name}}.md):
```markdown
## Changes made
- what was fixed

## Why it was wrong
- explanation referencing the source code
```

{phases}"""

DEFAULT_SYNC_PROMPT_PARALLEL = """Sync {count} docs by launching PARALLEL agents (one per doc).

Each agent will:
1. Read the doc + all related sources
2. Fix any outdated/incorrect content directly in the doc
3. Write a report to {syncs_dir}

Report format ({syncs_dir}/{{doc-name}}.md):
```markdown
## Changes made
- what was fixed

## Why it was wrong
- explanation referencing the source code
```

IMPORTANT: Launch ALL agents in a SINGLE message for parallel execution.

Docs to sync:

{docs_list}"""
