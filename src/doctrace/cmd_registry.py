from __future__ import annotations

from typing import TypedDict


class CommandInfo(TypedDict):
    desc: str
    args: str
    flags: list[str]
    subcommands: list[str]


COMMANDS: dict[str, CommandInfo] = {
    "info": {
        "desc": "show docs phases and warnings",
        "args": "<path>",
        "flags": ["--json", "--ignore"],
        "subcommands": [],
    },
    "affected": {
        "desc": "list docs affected by git diff",
        "args": "<path>",
        "flags": ["--since-base", "--last", "--base-branch", "--since", "--verbose", "-V", "--json", "--ignore"],
        "subcommands": [],
    },
    "preview": {
        "desc": "interactive docs explorer in browser",
        "args": "<path>",
        "flags": ["--port"],
        "subcommands": [],
    },
    "base": {
        "desc": "manage base commit state",
        "args": "<update|show>",
        "flags": [],
        "subcommands": ["update", "show"],
    },
    "init": {
        "desc": "create doctrace.json",
        "args": "",
        "flags": [],
        "subcommands": [],
    },
    "index": {
        "desc": "generate index.md from frontmatter",
        "args": "<path> -o <file>",
        "flags": ["-o", "--output"],
        "subcommands": [],
    },
    "completion": {
        "desc": "generate shell completion",
        "args": "<shell>",
        "flags": [],
        "subcommands": ["zsh", "bash", "fish"],
    },
}

DIR_COMMANDS = [c for c in COMMANDS if c not in ("base", "init", "completion")]
