# Sync Report: docs/guides/create-release.md

## Sources Checked

| Source | Exists | Notes |
|--------|--------|-------|
| .github/workflows/release.yml | yes | release workflow with 4 bump options |
| .changelog/ | yes | contains .gitkeep |
| pyproject.toml | yes | version 0.3.0, towncrier config with 3 fragment types |
| .bumpversion.cfg | yes | version 0.3.0, targets pyproject.toml |

## Related Docs Checked

| Doc | Exists | Notes |
|-----|--------|-------|
| docs/repo/cicd.md | yes | consistent with this guide |

## Changes Made

### 1. Fixed workflow actions order in release flow diagram

- **What**: The diagram listed "publish to PyPI" before "commit + tag"
- **Why**: In `.github/workflows/release.yml`, the actual step order is: bump version -> build changelog (towncrier) -> commit and tag -> build wheel -> publish to PyPI. The doc had publish before commit+tag, which is factually wrong.
- **Diff**: Swapped "publish to PyPI" and "commit + tag" lines in the ASCII diagram

### 2. Added missing `initial` bump type option

- **What**: The release flow diagram and step 3 instructions only listed "patch / minor / major"
- **Why**: `.github/workflows/release.yml` defines four choices: patch, minor, major, initial. The `initial` option was missing from the doc.
- **Diff**: Added "initial" to both the diagram text and step 3 instructions

## No Changes Needed

- **Frontmatter**: All sources and related_docs are accurate and exist
- **Tools section**: towncrier and bump2version are both confirmed in pyproject.toml dev deps and release workflow
- **Changelog fragments section**: Path pattern, types table, and example all match towncrier config in pyproject.toml
- **Commands section**: `make changelog-draft` target confirmed in Makefile
- **Trigger release steps**: Actions path and workflow name are accurate
