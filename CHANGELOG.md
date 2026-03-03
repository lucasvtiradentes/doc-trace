## 0.3.0 (2026-03-03)

### Features

- Add `--ignore` flag to `info` and `affected` commands to exclude files from analysis
- Add undeclared inline refs validation to `info` command - warns when docs/*.md referenced in body are not declared in related_docs

### Bug Fixes

- Fix circular_refs filter in affected command - was using string match instead of set membership
- Fix macOS symlink resolution in tests using tmppath.resolve()

### Misc

- Align `info` output format with shell script style (sections, headers, summary). Remove `--verbose` flag from `affected`, make verbose default. Rename "Independent" to "Level 0" in preview. Extract shared `matches_ignore_pattern` to core/filtering.py. Use sets for O(1) lookups in affected. Restructure README. Add pre-commit hooks and devpanel config.


## 0.2.3 (2026-03-01)

### Features

- add `doctrace completion` command for shell autocompletion (zsh/bash/fish) with full flag support
- add `doctrace index` command to generate index.md from frontmatter metadata

### Misc

- centralize command metadata in cmd_registry.py for CLI help and shell completions


## 0.2.2 (2026-02-19)

No significant changes.


## 0.2.1 (2026-02-18)

No significant changes.


## 0.2.0 (2026-02-17)

No significant changes.


## 0.1.2 (2026-02-17)

No significant changes.


## 0.1.1 (2026-02-17)

No significant changes.


## 0.1.0 (2026-02-17)

No significant changes.


# Changelog
