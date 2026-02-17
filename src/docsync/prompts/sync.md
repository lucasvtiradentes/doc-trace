Sync {count} docs by launching agents in phases (respecting dependencies).

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

{phases}
