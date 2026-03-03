# Sync Report: docs/repo/cicd.md

## Sources Checked
- .github/workflows/prs.yml
- .github/workflows/push-to-main.yml
- .github/workflows/callable-ci.yml
- .github/workflows/release.yml

## Related Docs Checked
- docs/repo/tooling.md

## Changes Made

### 1. Updated practical-test command in CI Jobs section
- **Location**: Line 57, under `### practical-test` code block
- **Reason**: The `doctrace info docs/` command in `callable-ci.yml` was updated (commit cb270b8) to include `--ignore docs/index.md`. The doc showed the old command without this flag.
- **Before**: `- doctrace info docs/`
- **After**: `- doctrace info docs/ --ignore docs/index.md`

## No Changes Needed
- Pipelines table: all workflow names, triggers, and purposes are accurate
- CI Jobs check section: steps match callable-ci.yml
- CI Jobs test section: Python version matrix (3.9, 3.12) and steps match callable-ci.yml
- Release Pipeline: steps and description match release.yml
- PyPI Publishing: uses `pypa/gh-action-pypi-publish` with trusted publisher, environment `pypi` - all correct
- Version Bump Options: patch, minor, major, initial all match release.yml
- Branch Strategy: accurate
- Frontmatter sources and related_docs: accurate, no changes needed
