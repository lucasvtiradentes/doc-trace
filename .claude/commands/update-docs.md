# Update Docs

Analyzes and updates documentation affected by code changes since a git reference.

## Usage

```
/update-docs <git-ref>
```

Examples:
- `/update-docs v1.0.0` - docs affected since tag v1.0.0
- `/update-docs HEAD~5` - docs affected by last 5 commits
- `/update-docs main` - docs affected since diverging from main
- `/update-docs --since-lock` - docs affected since last lock (incremental)

## Instructions

0. Create sync output directory: `.docsync/syncs/<timestamp>/` (format: `YYYY-MM-DDTHH-MM-SS`)

1. Run docsyncd affected to get affected docs:
   - If argument is `--since-lock`: `docsyncd affected docs/ --since-lock --verbose --json`
   - Otherwise: `docsyncd affected docs/ --since $ARGUMENTS --verbose --json`

2. Parse the JSON output to get:
   - `direct_hits` - docs directly affected by changed sources
   - `indirect_hits` - docs affected via references
   - `phases` - dependency order for processing
   - `git.commits` - commits in range (for context)
   - `git.source_to_docs` - which sources affect which docs

3. Process docs in phase order (phase 1 first, then 2, etc.) to respect dependencies

4. For each affected doc, spawn a subagent (Opus) to validate and update it:
   - Read the doc file
   - Read all files in `related sources:` section
   - Read all files in `related docs:` section
   - Compare doc content against source code
   - Identify outdated sections, missing info, or inaccuracies
   - Propose specific updates with explanations
   - Apply approved changes

5. Subagent prompt template:
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
8. For each issue found, propose a specific fix
9. Apply the fixes after explaining what you're changing
10. Write a report to {sync_dir}/{doc_name}.md with format:

## Confidence
high | medium | low

## Files read
- path/to/file.py - what you learned from it
- path/to/other.py - what you learned from it

## Changes made
- List each change made (or "No changes needed" if doc is up to date)

## Why it was wrong
- Explain what was outdated/incorrect and why, referencing specific source files

Be conservative - only change things that are clearly wrong or outdated.
Do not add comments or change formatting unless necessary.
```

6. Review phase (main agent):
   - Read all reports from `{sync_dir}/*.md`
   - Review what each subagent changed and why
   - Check for inconsistencies between related docs
   - If any change looks suspicious or incomplete, spawn a review agent (Opus) to:
     - Re-read the doc and sources
     - Validate the changes are correct
     - Fix any issues found
   - Ensure all docs are consistent with each other

7. After review, summarize:
   - Which docs were updated
   - What changes were made
   - Any docs that need manual review

8. Commit and lock:
   - Commit doc changes: `git add docs/ && git commit -m "docs: update affected docs"`
   - Run `docsyncd lock update` to save current commit
   - Amend to include lock: `git add .docsync/lock.json && git commit --amend --no-edit`

## Notes

- Uses Opus model for subagents to ensure high quality analysis
- Processes in dependency order so referenced docs are updated first
- Preserves main agent context by delegating to subagents
