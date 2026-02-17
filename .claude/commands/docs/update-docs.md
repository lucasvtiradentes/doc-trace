# Update Documentation (Legacy)

Read ALL source files in this repository and update documentation accordingly.

## Instructions

1. Read ALL files from these folders (in parallel):
   - `.github/` - Workflows and actions (check.yml, deploy.yml, terraform-deploy/action.yml)
   - `cloud-functions/` - Cloud function code (linear-webhook/, ai-triage-prunner/)
   - `infrastructure/` - Terraform files (*.tf)
   - `vm-payload/` - Runner scripts, templates, skills, docs

2. Also read root files:
   - `Makefile`
   - `README.md`
   - `CLAUDE.md`

3. Read ALL docs in `docs/` folder

4. Compare docs vs code field-by-field, update outdated sections

## Folders to Skip

- `.git/`, `.claude/`, `.ignore/`, `node_modules/`, `.devpanel/`
- `.terraform/`, `*.tfstate*`, `*.tfvars`, `*.lock.hcl`
- Binary files (images, videos)

## What to Update

- File structure diagrams (must match actual folders/files)
- Environment variables and secrets
- Constants and configuration values
- Function names and entry points
- New resources or removed resources

## How to Compare (CRITICAL)

Do NOT just eyeball docs and conclude "looks correct". For each doc file:

1. Identify every table, list, or reference to source code
2. Open the referenced source file
3. Compare EACH field/value/function name against the actual code
4. Check for missing items (new functions, new env vars, new constants not in docs)
5. Check for removed items (functions/vars that no longer exist in code)

Examples of things to verify field-by-field:
- Normalized LINEAR_* variables table → compare every row against `lib/payload.js` normalizeLinearPayload()
- Function tables → compare every function name against actual exports in each .js/.sh file
- Constants tables → compare every value against `runner/config.sh` and `lib/config.js`
- Template variables → compare against actual `{{PLACEHOLDER}}` usage in source files
- VM metadata list → compare against metadata items built in `index.js`
- Environment variables → compare against actual exports in `bootstrap.sh` and `setup.sh`
- File structure tree → compare against actual files on disk via Glob
- Request flow steps → compare against actual code execution order
- Repo config mappings → compare against `repos/config.json` and `repos/resolve.sh`

## Style Rules

- Keep docs concise, no fluff
- Tables must be aligned (equal column spacing)
- ASCII diagrams must have consistent box widths
- Use existing format as reference
- No emojis unless already present
- English only

## Table Format Example

```md
| Column One | Column Two | Column Three |
|------------|------------|--------------|
| value      | value      | value        |
| longer val | short      | medium value |
```

## Diagram Alignment

- Box borders must align vertically
- Inner content must have consistent padding
- Use `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼` for borders

## Files to Check

- docs/overview.md
- docs/infrastructure.md
- docs/cicd.md
- docs/development-rules.md
- docs/steps/*.md

## Final Step: Alignment Verification

After ALL content updates are done, run the `/docs:fix-docs-alignment` skill to detect and fix alignment issues in tables and ASCII diagrams.

## Output

After updates, list what changed in each file.
