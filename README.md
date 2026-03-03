<a name="TOC"></a>

<h1 align="center">doctrace</h1>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-motivation">Motivation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

<div width="100%" align="center">
  <img src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/divider.png" />
</div>

## 🎺 Overview<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

Keep documentation in sync with code. When files change, know exactly which docs need review - and in what order.

```
  src/booking/handler.ts changed
               │
               v
      ┌───────────────────┐
      │ doctrace affected │
      └────────┬──────────┘
               │
               v
  ┌─────────────────────────────────┐
  │ Direct hits:                    │
  │   docs/bookings.md              │  ← has "sources: src/booking/"
  │                                 │
  │ Indirect hits:                  │
  │   docs/payments.md              │  ← requires docs/bookings.md
  └─────────────────────────────────┘
```

<div align="center">
<details>
<summary>Preview</summary>
<img src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/preview.png" width="650" />
</details>
</div>

<div align="center">
<details>
<summary>How it works</summary>
<div align="left">

Each doc has YAML frontmatter with metadata sections:

```markdown
---
required_docs:
  - docs/payments.md: payment integration

sources:
  - src/booking/: booking module
  - src/booking/commands/: command handlers
---

# Booking System

How bookings work...
```

When `src/booking/handler.ts` changes:

```
doctrace affected docs/ --last 1

Direct hits (1):
  docs/bookings.md       <- references src/booking/

Indirect hits (1):
  docs/payments.md       <- referenced BY docs/bookings.md
```

The propagation: if `bookings.md` might be outdated, then `payments.md` (which references it) might also need review.

</div>
</details>
</div>

## ⭐ Features<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

- **Impact analysis**: detects which docs need review when code changes, with cascading through dependencies
- **AI-ready output**: JSON output feeds AI agents to auto-update docs based on code changes
- **Interactive UI**:  browser dashboard to explore and visualize doc dependencies
- **Auto-gen index**:  generates index.md table from frontmatter metadata

## ❓ Motivation<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

In large codebases, docs get outdated because:

1. No one remembers which docs need updating when a file changes
2. AI agents don't know which files to read to understand each doc

doctrace solves this by adding "hints" to each doc - `sources:` tells any AI exactly what to read.

## 🚀 Quick Start<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

Install:

```bash
brew install pipx         # if not installed (macOS/linux)
pipx install doctrace     # or: pip install doctrace
```

Add metadata to your docs:

```markdown
---
required_docs:
  - docs/other-feature.md: hard dependency

related_docs:
  - docs/related.md: soft reference

sources:
  - src/feature/: main module
  - src/feature/utils.ts: helper functions
---

# My Feature

Documentation content here...
```

Setup in your repo:

```bash
cd your-repo
doctrace init                        # creates doctrace.json (optional)

doctrace info docs/                  # show phases + validate refs
doctrace affected docs/ --last 5     # find docs affected by last 5 commits
doctrace preview docs/               # interactive explorer in browser
```

## 📖 Commands<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

```bash
doctrace info <path>                           # show phases + validate refs
doctrace affected <path> --last <N>            # list affected docs by last N commits
doctrace affected <path> --since <ref>         # list affected docs since ref (commit/tag/branch)
doctrace affected <path> --base-branch <branch># list affected docs from merge-base
doctrace affected <path> --json                # output as JSON
doctrace preview <path>                        # interactive explorer in browser
doctrace preview <path> --port <N>             # preview on custom port (default 8420)
doctrace init                                  # create doctrace.json
doctrace index <path> -o <file>                # generate index.md from frontmatter
doctrace completion <shell>                    # generate shell completion script
doctrace --version                             # show version
```

<div align="center">
<details>
<summary>Example output</summary>
<div align="left">

```
Direct hits (3):
  docs/concepts.md
  docs/api.md
  docs/utils.md

Indirect hits (1):
  docs/overview.md <- docs/api.md

Phases (3):
  1. docs/concepts.md, docs/utils.md
  2. docs/api.md
  3. docs/overview.md
```

Phases show dependency order - useful for AI agents processing docs.

</div>
</details>
</div>

## ⚙️ Configuration<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

<div align="center">
<details>
<summary>Config file</summary>
<div align="left">

`doctrace.json` (at repo root):

```json
{
  "metadata": {
    "required_docs_key": "required_docs",
    "related_docs_key": "related_docs",
    "sources_key": "sources"
  }
}
```

| Key                          | Description                                                  |
|------------------------------|--------------------------------------------------------------|
| `metadata.required_docs_key` | frontmatter key for required docs (default: "required_docs") |
| `metadata.related_docs_key`  | frontmatter key for related docs (default: "related_docs")   |
| `metadata.sources_key`       | frontmatter key for source refs (default: "sources")         |

</div>
</details>
</div>

<div align="center">
<details>
<summary>Shell Completion</summary>
<div align="left">

```bash
# zsh - add to ~/.zshrc
eval "$(doctrace completion zsh)"

# bash - add to ~/.bashrc
eval "$(doctrace completion bash)"

# fish
doctrace completion fish | source
```

</div>
</details>
</div>

## 🤝 Contributing<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

```bash
make install    # venv + deps + pre-commit
make test       # run tests
make format     # ruff fix + format
make check      # validate ruff rules
make build      # build package
make clean      # remove venv + dist
```

Dev alias:

```bash
ln -sf $(pwd)/.venv/bin/doctrace ~/.local/bin/doctraced   # install
rm ~/.local/bin/doctraced                                 # remove
```

## 📜 License<a href="#TOC"><img align="right" src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/up_arrow.png" width="22"></a>

This project is licensed under the [MIT License](LICENSE).

<div width="100%" align="center">
  <img src="https://cdn.jsdelivr.net/gh/lucasvtiradentes/doc-trace@main/.github/images/divider.png" />
</div>

<br />

<div align="center">
  <a target="_blank" href="https://www.linkedin.com/in/lucasvtiradentes/"><img src="https://img.shields.io/badge/-linkedin-blue?logo=Linkedin&logoColor=white" alt="LinkedIn"></a>
  <a target="_blank" href="mailto:lucasvtiradentes@gmail.com"><img src="https://img.shields.io/badge/-email-red?logo=Gmail&logoColor=white" alt="Email"></a>
  <a target="_blank" href="https://github.com/lucasvtiradentes"><img src="https://img.shields.io/badge/-github-gray?logo=Github&logoColor=white" alt="GitHub"></a>
</div>
