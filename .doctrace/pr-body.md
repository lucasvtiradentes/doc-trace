## Summary

13 docs updated since `docs-base`, all high confidence.

```
 docs/architecture.md          | 53 +++++++++++++++++++++----------------------
 docs/concepts.md              | 13 +++++++----
 docs/features/affected.md     |  1 +
 docs/features/index-cmd.md    | 14 ++++++------
 docs/features/preview.md      |  2 +-
 docs/features/validation.md   | 42 ++++++++++++++++++++++------------
 docs/guides/create-release.md |  6 ++---
 docs/overview.md              |  2 +-
 docs/repo/cicd.md             |  2 +-
 docs/repo/local-setup.md      |  8 ++++---
 docs/repo/structure.md        | 11 +++++++--
 docs/rules.md                 | 16 +++++++------
 docs/testing.md               |  4 ++--
 13 files changed, 101 insertions(+), 73 deletions(-)
```

<div align="center">

| Doc | Changes | Metadata |
|-----|---------|----------|
| `docs/architecture.md` | 5 fixes (diagrams, module tree, pseudocode) | - |
| `docs/concepts.md` | 2 fixes (ParsedDoc fields, RefError field) | - |
| `docs/features/affected.md` | No content changes | +1 source |
| `docs/features/completion.md` | No changes needed | - |
| `docs/features/index-cmd.md` | 3 fixes (sort order, output format, function name) | - |
| `docs/features/initialization.md` | No changes needed | - |
| `docs/features/preview.md` | 1 fix (removed nonexistent created date) | - |
| `docs/features/validation.md` | 5 fixes (output format, exit codes, config) | - |
| `docs/guides/create-release.md` | 2 fixes (workflow order, initial bump type) | - |
| `docs/overview.md` | 1 fix (version 0.1.1 -> 0.3.0) | - |
| `docs/repo/cicd.md` | 1 fix (--ignore flag in practical-test) | - |
| `docs/repo/local-setup.md` | 3 fixes (pre-commit, make install, practical-test) | +1 related doc |
| `docs/repo/structure.md` | 5 additions (new files in tree listing) | - |
| `docs/repo/tooling.md` | No changes needed | - |
| `docs/rules.md` | 4 fixes (commands list, validate->info, depth_limit) | - |
| `docs/testing.md` | 2 fixes (inline refs coverage, practical-test) | - |

</div>

## Source

<details>
<summary>30 commits in range</summary>

**Range**: `9f0c964..e919a76`

<div align="center">

| Hash | Author | Message |
|------|--------|---------|
| e919a76 | github-actions[bot] | chore: release v0.3.0 |
| ae520e5 | Lucas Vieira | chore: update gitignore |
| 85327e0 | Lucas Vieira | Merge branch 'chore/small_refactors_v3' |
| be3c24a | Lucas Vieira | chore: update docs |
| 20e5080 | Lucas Vieira | refactor: remove base command and --since-base flag |
| e655d9b | Lucas Vieira | chore: update readme |
| cb270b8 | Lucas Vieira | fix: cicd error |
| 8b11f92 | Lucas Vieira | Merge branch 'chore/small_refactors_v2' |
| ef1c555 | Lucas Vieira | chore: add changelog fragments for release |
| b9ec29c | Lucas Vieira | chore: remove python expert agent file |
| c250e10 | Lucas Vieira | chore: add pre-commit, devpanel, fix test symlinks |
| c68c970 | Lucas Vieira | refactor(preview): rename Independent to Level 0 |
| 109efb7 | Lucas Vieira | docs: remove --verbose references, add --ignore to completion |
| 89d4495 | Lucas Vieira | refactor(affected): remove --verbose flag, make verbose default |
| 706a305 | Lucas Vieira | refactor: extract fnmatch filter to core/filtering.py |
| 5a7b78b | Lucas Vieira | refactor(info): remove bidirectional refs + add affected ignore tests |
| 511478d | Lucas Vieira | refactor(info): align output format with shell script |
| d7935cc | Lucas Vieira | feat(info): add ignore_inline_refs config and --ignore flag |
| 26333da | Lucas Vieira | refactor(info): remove bidirectional validation |
| 2cac932 | Lucas Vieira | feat(info): add undeclared inline refs validation |
| b749980 | Lucas Vieira | feat(info): add bidirectional related_docs validation |
| 12c9205 | Lucas Vieira | docs: refactor README to match branch-context style |
| e1d2e82 | github-actions[bot] | chore: release v0.2.3 |
| 8b23b79 | Lucas Vieira | Merge branch 'chore/small_refactors_v1' |
| 5ae1b9c | Lucas Vieira | chore: add release guide |
| 88ce452 | Lucas Vieira | docs: add index and completion commands to documentation |
| 6daaede | Lucas Vieira | refactor: centralize command metadata in cmd_registry |
| a840728 | Lucas Vieira | feat: add completion command for shell autocompletion |
| 0ebacd1 | Lucas Vieira | feat: add index command to generate index.md from frontmatter |
| 9f0c964 | Lucas Vieira | chore: add bctx tool |

</div>

**Related PRs**: None

</details>

## What Changed

**Key themes**: Major validation overhaul (inline refs, --ignore flag), two new commands (index, completion), cmd_registry centralization, and various refactors removing deprecated features (base command, --verbose flag, bidirectional validation).

<details>
<summary>Changes by doc (16 docs)</summary>

### docs/architecture.md
- Added `index` and `completion` to entry point dispatcher diagram
- Fixed `preview.py` to `preview/` (it's a package)
- Added `cmd_registry.py`, `completion.py`, `index.py`, `filtering.py` to module tree
- Fixed `_build_indexes()` to `build_doc_index()` and `doc_to_docs` to `reverse_deps`
- Removed `depth_limit` from propagation pseudocode, added `_find_circular_refs()` call

### docs/concepts.md
- Added `title` and `description` fields to ParsedDoc table
- Added `ref_type` field to RefError table

### docs/features/affected.md
- Added `src/doctrace/core/filtering.py` to frontmatter sources

### docs/features/completion.md
- No changes needed (doc is up to date)

### docs/features/index-cmd.md
- Fixed sort description from "sorted by filename" to "sorted by category, then filename"
- Updated output example to show 6-column table matching actual output
- Fixed `get_docs_metadata()` to `build_doc_index()`

### docs/features/initialization.md
- No changes needed (doc is up to date)

### docs/features/preview.md
- Removed "created date" from doc stats (not rendered in UI)

### docs/features/validation.md
- Updated error output section to match new format with section headers
- Broadened exit code 1 description to include all error types
- Updated output format example to match structured report
- Fixed `ignored_paths` to `ignore_inline_refs` config + `--ignore` CLI patterns
- Changed parse error behavior from "reports" to "silently skips"

### docs/guides/create-release.md
- Fixed workflow actions order (commit+tag before publish)
- Added missing `initial` bump type option

### docs/overview.md
- Updated version from 0.1.1 to 0.3.0

### docs/repo/cicd.md
- Added `--ignore docs/index.md` to practical-test command

### docs/repo/local-setup.md
- Added `pre-commit` to dev dependencies table
- Updated `make install` to mention pre-commit hook installation
- Updated `make practical-test` with --ignore flag
- Added `docs/index.md` to related_docs (inline ref fix)

### docs/repo/structure.md
- Added `cmd_registry.py`, `completion.py`, `index.py`, `filtering.py` to tree
- Added `core/` to tests tree, `update-docs.yml` to workflows tree

### docs/repo/tooling.md
- No changes needed (doc is up to date)

### docs/rules.md
- Added `index` and `completion` to single-responsibility commands list
- Fixed `validate` to `info` in lazy error recovery section
- Fixed lowercase CLI command list to match actual commands
- Removed nonexistent `affected_depth_limit` reference

### docs/testing.md
- Added inline refs to validate test coverage description
- Updated practical-test command with --ignore flag

</details>

## Validation

- Circular deps: none
- Broken refs: none

## Documentation Gaps

<details>
<summary>15 changes analyzed, 2 need attention</summary>

<div align="center">

| # | Impact | Change | Status | Notes |
|---|--------|--------|--------|-------|
| 1 | feature | completion command | covered | `docs/features/completion.md` |
| 2 | feature | index command | covered | `docs/features/index-cmd.md` |
| 3 | feature | inline refs validation | covered | updated `docs/features/validation.md` |
| 4 | feature | --ignore flag for info | covered | updated `docs/features/validation.md` |
| 5 | feature | --ignore flag for affected | partial | `docs/features/affected.md` doesn't document it |
| 6 | refactor | cmd_registry centralization | covered | `docs/features/completion.md`, `docs/repo/structure.md` |
| 7 | refactor | remove --verbose flag | covered | `docs/features/affected.md` already correct |
| 8 | refactor | remove base command | covered | was never documented |
| 9 | refactor | rename Independent to Level 0 | covered | `docs/features/preview.md` verified |
| 10 | refactor | extract filtering.py | covered | `docs/repo/structure.md`, `docs/features/affected.md` |
| 11 | fix | cicd --ignore flag | covered | `docs/repo/cicd.md` updated |
| 12 | minor | pre-commit added | partial | `docs/repo/local-setup.md` updated, `docs/repo/tooling.md` not |
| 13 | minor | release v0.3.0 | covered | `docs/overview.md` version updated |
| 14 | minor | release guide | covered | `docs/guides/create-release.md` |
| 15 | minor | gitignore, bctx, devpanel | no-doc | internal tooling/config |

</div>

**Legend:** missing (needs new doc), partial (needs update), covered (done), no-doc (not needed)

</details>

## Action Needed

<div align="center">

| # | Change | Suggested Action |
|---|--------|------------------|
| 5 | --ignore flag for affected | Add `--ignore` to flags list in `docs/features/affected.md` |
| 12 | pre-commit tooling | Add pre-commit section to `docs/repo/tooling.md` |

</div>
