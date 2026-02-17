## Changes made
- Rewrote test layout and coverage sections to reflect current nested `tests/*/` structure.
- Updated examples/pattern notes to match actual test techniques used now.
- Kept CI-equivalent local commands aligned with Makefile targets.

## Why it was wrong
- Existing doc referenced obsolete flat test files (`test_cascade.py`, etc.) that do not exist.
- Current suite is organized under directories like `tests/cascade/`, `tests/check/`, `tests/parser/`, `tests/prompt/`, `tests/tree/`, and `tests/config/`.
