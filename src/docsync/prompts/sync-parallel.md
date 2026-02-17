Sync {count} docs by launching PARALLEL agents (one per doc).

Each agent will:
1. Read the doc + all related sources
2. Fix any outdated/incorrect content directly in the doc
3. Write a report to {syncs_dir}

Report format ({syncs_dir}/{{doc-name}}.md):
```markdown
## Changes made
- what was fixed

## Why it was wrong
- explanation referencing the source code
```

IMPORTANT: Launch ALL agents in a SINGLE message for parallel execution.

Docs to sync:

{docs_list}
