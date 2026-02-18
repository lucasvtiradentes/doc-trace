## Confidence
high

## Files read
- docs/guides/setup-project.md - validated install, verify, and command sections.
- pyproject.toml - confirmed current project version is 0.1.1 and dev dependency constraints.
- Makefile - confirmed documented make commands exist.
- docs/repo/local-setup.md - checked consistency of installation guidance.

## Metadata updates
No metadata changes

## Changes made
- Updated verify-installation expected output to match current installed version semantics (`docsync 0.1.1` example).

## Why it was wrong
The doc hard-coded `docsync 0.1.0`, but the current `project.version` in `pyproject.toml` is `0.1.1`, so the expected output example was stale.
