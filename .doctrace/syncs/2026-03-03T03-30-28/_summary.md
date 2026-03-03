# Sync Summary: 2026-03-03T03-30-28

## Range
- **Base**: `docs-base` (`70bbde3`)
- **Head**: `85327e0`
- **Commits**: 20

## Docs Processed: 15

### Phase 1 (12 docs)
| Doc | Changes | Confidence |
|-----|---------|------------|
| docs/concepts.md | 1 fix (added ref_type field to RefError table) | high |
| docs/features/completion.md | No changes | high |
| docs/features/initialization.md | No changes | high |
| docs/features/preview.md | No changes | high |
| docs/guides/create-release.md | No changes | high |
| docs/overview.md | 1 fix (version 0.1.1 -> 0.2.3) | high |
| docs/repo/cicd.md | 1 fix (added --ignore flag to practical-test command) | high |
| docs/repo/local-setup.md | 5 fixes (pre-commit dep, make install desc, make format, make practical-test, make build/clean) | high |
| docs/repo/structure.md | 3 fixes (removed base state from config.py desc, added filtering.py to tree and prose) | high |
| docs/repo/tooling.md | No changes | high |
| docs/rules.md | 2 fixes (corrected command list, removed nonexistent affected_depth_limit) | high |
| docs/testing.md | 1 fix (added inline refs to validate/ coverage description) | high |

### Phase 2 (3 docs)
| Doc | Changes | Confidence |
|-----|---------|------------|
| docs/architecture.md | 3 fixes (phases->levels in info desc, added filtering.py, removed depth_limit from propagation) | high |
| docs/features/affected.md | 1 fix (added filtering.py to frontmatter sources) | high |
| docs/features/validation.md | 9 fixes (major update: levels terminology, --ignore flag, inline ref validation, output format, exit codes, implementation table) | high |

### Post-validation fix
| Doc | Change |
|-----|--------|
| docs/repo/local-setup.md | Wrapped CLI argument `docs/index.md` in backticks to avoid false inline ref detection |

## Validation Results
- Circular deps: none
- Broken refs: none
- Undeclared inline refs: none (after fix)

## Gap Analysis

| # | Impact | Change | Status | Notes |
|---|--------|--------|--------|-------|
| 1 | feature | inline refs validation (info) | covered | docs/features/validation.md updated |
| 2 | feature | --ignore flag (info + affected) | covered | docs/features/validation.md, docs/features/affected.md |
| 3 | feature | ignore_inline_refs config | partial | docs/rules.md mentions config but doesn't list this key |
| 4 | refactor | remove base command | covered | no docs referenced it |
| 5 | refactor | remove --since-base flag | covered | no docs referenced it |
| 6 | refactor | remove --verbose flag (affected) | covered | no docs referenced it |
| 7 | refactor | rename Independent to Level 0 | covered | no docs used "Independent" |
| 8 | refactor | extract filtering.py | covered | docs/repo/structure.md, docs/features/affected.md updated |
| 9 | refactor | info output format (levels, sections) | covered | docs/features/validation.md updated |
| 10 | fix | cicd --ignore flag | covered | docs/repo/cicd.md updated |
| 11 | minor | add pre-commit | covered | docs/repo/local-setup.md updated |
| 12 | minor | rename make fix to format | covered | docs/repo/local-setup.md updated |
| 13 | minor | add make build/clean targets | covered | docs/repo/local-setup.md updated |
| 14 | minor | update-docs.yml git_ref input | no-doc | CI workflow detail |
| 15 | minor | add devpanel config | no-doc | dev tooling |
| 16 | minor | add changelog fragments | no-doc | release housekeeping |
| 17 | minor | remove python expert agent | no-doc | internal tooling |
| 18 | minor | README refactor | no-doc | standalone file |
| 19 | minor | delete doctrace.json | covered | no docs referenced it |
| 20 | minor | version bump to 0.2.3 | covered | docs/overview.md updated |
