## Changes made
- Removed unsupported claim that `main` is protected and kept branch strategy statements source-backed.

## Why it was wrong
- Protection status is not defined in `.github/workflows/prs.yml`, `.github/workflows/push-to-main.yml`, `.github/workflows/callable-ci.yml`, or `.github/workflows/release.yml`.
