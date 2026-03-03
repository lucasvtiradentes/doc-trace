# Sync Report: docs/repo/cicd.md

## Changes Applied

### 1. Updated `doctrace info` command in practical-test section
- **Location**: Line 57, practical-test code block
- **Source**: `.github/workflows/callable-ci.yml` line 26
- **Before**: `doctrace info docs/`
- **After**: `doctrace info docs/ --ignore docs/index.md`
- **Reason**: The `--ignore docs/index.md` flag was added in commit cb270b8 ("fix: cicd error"). The doc did not reflect this argument.

## No Changes Needed

- **Pipelines table**: All workflow names, triggers, and purposes match source files.
- **check job**: Steps match `callable-ci.yml` lines 10-16.
- **test job**: Python version matrix (3.9, 3.12) and steps match `callable-ci.yml` lines 28-39.
- **Release pipeline**: Steps, tools, version bump options, and PyPI publishing details all match `release.yml`.
- **Branch strategy**: Matches `push-to-main.yml` trigger configuration.
- **Frontmatter sources**: All listed source files exist and are relevant.
- **related_docs**: `docs/repo/tooling.md` exists and is relevant.

## Notes

- The `update-docs.yml` workflow (which changed in this range with a new `git_ref` input parameter) is not documented in this file nor listed in its sources. This is not a factual error in the existing content -- it is simply a workflow not covered by this doc. No change was made.
- The job order in the doc (check, test, practical-test) differs from the YAML file order (check, practical-test, test). This is not a factual error since the doc does not claim execution ordering, so no reordering was applied.
