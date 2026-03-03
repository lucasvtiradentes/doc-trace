---
title: Completion Command
description: Generates shell completion scripts for zsh, bash, and fish
related_docs:
  - docs/overview.md: CLI commands overview
sources:
  - src/doctrace/commands/completion.py: completion generators
  - src/doctrace/cmd_registry.py: command metadata
---

Generates shell completion scripts with full support for commands, subcommands, flags, and directory paths.

## Usage

```bash
doctrace completion zsh   # generate zsh completion
doctrace completion bash  # generate bash completion
doctrace completion fish  # generate fish completion
```

## Installation

Add to your shell config:

```bash
# zsh (~/.zshrc)
eval "$(doctrace completion zsh)"

# bash (~/.bashrc)
eval "$(doctrace completion bash)"

# fish (~/.config/fish/config.fish)
doctrace completion fish | source
```

## What Gets Completed

| Context                    | Completions                              |
|----------------------------|------------------------------------------|
| `doctrace <TAB>`           | all commands                             |
| `doctrace info <TAB>`      | directories                              |
| `doctrace info --<TAB>`    | `--json --ignore`                        |
| `doctrace affected --<TAB>`| `--since-base --last --json --ignore`   |
| `doctrace base <TAB>`      | `update show`                            |
| `doctrace completion <TAB>`| `zsh bash fish`                          |
| `doctrace index --<TAB>`   | `-o --output`                            |

## Implementation

Uses `cmd_registry.py` as single source of truth for:
- Command descriptions
- Flags per command
- Subcommands per command
- Which commands accept directory paths

Shell-specific generators produce completion scripts dynamically from this registry.
