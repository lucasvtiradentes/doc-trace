## Confidence
high

## Files read
- src/docsync/cli.py - entry point, verified commands (validate, affected, preview, lock, init) and their args
- src/docsync/commands/affected.py - verified AffectedResult, --json flag, --verbose flag, data-first architecture
- src/docsync/commands/preview/__init__.py - confirmed preview is a package re-exporting server.run
- src/docsync/commands/preview/server.py - confirmed http.server, socketserver, threading, webbrowser usage
- src/docsync/commands/preview/graph.py - confirmed json usage for preview API
- src/docsync/commands/preview/tree.py - confirmed tree module still exists (refactored from command to internal)
- src/docsync/commands/preview/search.py - confirmed search functionality
- src/docsync/commands/validate.py - confirmed fnmatch usage
- src/docsync/commands/lock.py - confirmed lock subcommands (update, show)
- src/docsync/commands/init.py - confirmed init command
- src/docsync/core/git.py - confirmed subprocess usage, new functions (get_file_history, get_file_at_commit, get_commits_in_range, etc.)
- src/docsync/core/constants.py - confirmed re usage for patterns
- src/docsync/core/config.py - confirmed json usage for config
- src/docsync/core/lock.py - confirmed json usage for lock
- src/docsync/core/parser.py - confirmed re usage for parsing
- pyproject.toml - confirmed version is 0.1.1, not 0.1.0
- docs/architecture.md - related doc, verified consistency
- docs/concepts.md - related doc, verified consistency
- All 16 docs in index verified to exist on disk

## Metadata updates
No metadata changes

## Changes made
- Updated version from 0.1.0 to 0.1.1 in Package Info table
- Updated json description from "config/lock file handling" to "config/lock/output handling" (json is now also used for --json flag output and preview API responses)

## Why it was wrong
- Version 0.1.0 was outdated: pyproject.toml shows 0.1.1, and the v0.1.1 tag exists in the git history
- The json module description was incomplete: commits e9407ea (add --json flag) and f04e6fa (refactor preview command) added json usage for CLI output and HTTP API responses, not just config/lock files
