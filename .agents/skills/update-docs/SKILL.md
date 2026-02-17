---
name: update-docs
description: Analyze and update documentation affected by code changes since a git reference using docsyncd. Use when the user asks to refresh docs after commits, update docs since a tag/branch/commit range, run incremental sync with --since-lock, validate doc references, and produce a consolidated sync report.
---

# Update Docs

Analyzes and updates documentation affected by code changes since a git reference.

## Usage

```bash
update-docs <git-ref>
```

Examples:
- `update-docs v1.0.0` - docs affected since tag v1.0.0
- `update-docs HEAD~5` - docs affected by last 5 commits
- `update-docs main` - docs affected since diverging from main
- `update-docs --since-lock` - docs affected since last lock (incremental)

## Instructions

### Mandatory Execution Model

- Use **one main agent** (parent/orchestrator) for the whole run.
- The main agent **must spawn subagents** for doc analysis work.
- For every affected doc in a phase, spawn **exactly 1 subagent per doc**.
- The main agent **must not** do per-doc validation/update work itself, except re-checking suspicious results.

0. Create sync output directory: `.docsync/syncs/<timestamp>/` (format: `YYYY-MM-DDTHH-MM-SS`)

1. Run `docsyncd affected` to get affected docs:
   - If argument is `--since-lock`: `docsyncd affected docs/ --since-lock --verbose --json`
   - Otherwise: `docsyncd affected docs/ --since <git_ref> --verbose --json`

2. Parse the JSON output to get:
   - `direct_hits` - docs directly affected by changed sources
   - `indirect_hits` - docs affected via references
   - `phases` - dependency order for processing
   - `git.commits` - commits in range (for context)
   - `git.source_to_docs` - which sources affect which docs

3. Process docs in phase order (phase 1 first, then 2, etc.) to respect dependencies.
   Within each phase, run doc analysis tasks in parallel using subagents orchestrated by the main agent.
   - Launch exactly 1 subagent per affected doc in that phase.
   - Subagents execute the per-doc prompt; main agent only coordinates.
   - Do not process docs from the next phase until all subagents in the current phase finish.
   - The parent agent is responsible for orchestration, conflict handling, and final validation.

4. For each affected doc, the assigned subagent must run a focused validation/update pass:
   - Read the doc file
   - Read all files in `related sources:` section
   - Read all files in `related docs:` section
   - Compare doc content against source code
   - Identify outdated sections, missing info, or inaccuracies
   - Update metadata if sources/docs changed
   - Apply changes
   - Write the per-doc report to `{sync_dir}/{doc_name}.md`

5. Per-doc prompt template:
```md
You are validating and updating a documentation file.

Doc to validate: {doc_path}
Output report: {sync_dir}/{doc_name}.md

## Git context

Changed files since {git_ref}:
{changed_files_verbose}

Commits in range:
{commits_list}

This doc was flagged because these sources changed:
{matched_sources}

## Your task

1. Read the doc file
2. Read all related sources listed in the doc's metadata
3. Read all related docs listed in the doc's metadata
4. Use git context above to understand what changed and why
5. Feel free to explore beyond listed sources if needed (imports, dependencies, related modules)
6. Compare the doc content against the actual source code
7. Identify any:
   - Outdated information
   - Missing features or changes
   - Inaccurate descriptions
   - Broken references
8. Update metadata if needed:
   - Remove sources that no longer exist or are no longer relevant
   - Add new sources you discovered that this doc depends on
   - Remove related docs that no longer exist
   - Add related docs you discovered that are closely related
9. For each issue found, propose a specific fix
10. Apply the fixes after explaining what you're changing
11. Write a report to {sync_dir}/{doc_name}.md with format:

## Confidence
high | medium | low

## Files read
- path/to/file.py - what you learned from it

## Metadata updates
- Added source: path/to/new.py (reason)
- Removed source: path/to/old.py (deleted/no longer relevant)
- Added related doc: docs/other.md (reason)
- (or "No metadata changes")

## Changes made
- List each change made (or "No changes needed" if doc is up to date)

## Why it was wrong
- Explain what was outdated/incorrect and why, referencing specific source files

Be conservative - only change things that are clearly wrong or outdated.
Do not add comments or change formatting unless necessary.
```

6. Review phase (parent agent):
   - Read all reports from `{sync_dir}/*.md`
   - Check for any report with `Confidence: low` and run a second review pass
   - Check for inconsistencies between related docs
   - If any change looks suspicious, re-validate before finalizing

7. Run validation (parent agent):
   - Execute `docsyncd validate docs/` to check for broken refs
   - If errors are found, fix them before proceeding

8. Generate consolidated report (parent agent):
   - Write `{sync_dir}/summary.md` with format:
```md
# Doc Sync Summary

Run: {timestamp}
Reference: {git_ref}
Docs analyzed: {count}

## Changes by doc

| Doc | Confidence | Changes | Metadata |
|-----|------------|---------|----------|
| docs/foo.md | high | 2 content, 1 metadata | +1 source |
| docs/bar.md | high | No changes | - |

## All changes

### docs/foo.md
- Updated X to Y (reason)
- Added source: path/to/new.py

### docs/bar.md
- No changes needed

## Validation
- Status: passed | failed
- Errors: (if any)
```

9. Summarize to user (parent agent):
   - Which docs were updated
   - What changes were made
   - Any docs that need manual review (low confidence)

10. Commit and lock only if the user explicitly asks:
    - Commit doc changes: `git add docs/ && git commit -m "docs: update affected docs"`
    - Run `docsyncd lock update` to save current commit
    - Commit lock update: `git add .docsync/lock.json && git commit -m "docsync: update lock"`

## Notes

- Non-negotiable: this skill is a **main-agent + subagents** workflow, not a single-agent workflow.
- Process phases sequentially (dependencies), launching one subagent per doc inside each phase
- Low confidence reports trigger automatic re-validation
- Validate refs after updates to catch broken links early
- Consolidated summary enables easy PR review
