# Doc Sync Summary - 2026-03-03T03-48-59

## Range
- **Git ref**: `docs-base`
- **Base commit**: `9f0c964`
- **Head commit**: `e919a76`
- **Commits**: 30

## Docs Processed: 16

### Phase 1 (13 docs)
| Doc | Changes | Confidence |
|-----|---------|------------|
| `docs/concepts.md` | 2 fixes: added ParsedDoc title/description fields, added RefError ref_type field | high |
| `docs/features/completion.md` | No changes needed | high |
| `docs/features/index-cmd.md` | 3 fixes: sort order, output format, function name | high |
| `docs/features/initialization.md` | No changes needed | high |
| `docs/features/preview.md` | 1 fix: removed nonexistent "created date" from doc stats | high |
| `docs/guides/create-release.md` | 2 fixes: workflow order, added initial bump type | high |
| `docs/overview.md` | 1 fix: version 0.1.1 -> 0.3.0 | high |
| `docs/repo/cicd.md` | 1 fix: added --ignore docs/index.md to practical-test | high |
| `docs/repo/local-setup.md` | 3 fixes: added pre-commit dep, updated make install, updated practical-test | high |
| `docs/repo/structure.md` | 5 fixes: added cmd_registry.py, completion.py, index.py, filtering.py, core/ tests, update-docs.yml | high |
| `docs/repo/tooling.md` | No changes needed | high |
| `docs/rules.md` | 4 fixes: added index/completion commands, fixed validate->info, fixed command list, removed nonexistent affected_depth_limit | high |
| `docs/testing.md` | 2 fixes: added inline refs to validate coverage, updated practical-test command | high |

### Phase 2 (3 docs)
| Doc | Changes | Confidence |
|-----|---------|------------|
| `docs/architecture.md` | 5 fixes: entry point diagram, module tree, affected data flow, propagation pseudocode | high |
| `docs/features/affected.md` | 1 fix: added filtering.py to frontmatter sources | high |
| `docs/features/validation.md` | 5 fixes: error output format, exit codes, output format, ignore config, parse behavior | high |

### Post-processing
- Fixed 1 broken inline ref: `docs/repo/local-setup.md -> docs/index.md` (added to related_docs)

## Validation Results
- Circular deps: 0
- Missing refs: 0
- Missing inline refs: 0

## Documentation Gaps

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
