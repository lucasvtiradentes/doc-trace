import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from doctrace.cmd_registry import COMMANDS
from doctrace.commands import affected, base, completion, index, info, init, preview
from doctrace.core.constants import DEFAULT_PREVIEW_PORT

VERSION = version("doctrace")


def main():
    parser = argparse.ArgumentParser(description="Keep docs in sync with code")
    parser.add_argument("-v", "--version", action="version", version=f"doctrace {VERSION}")
    subparsers = parser.add_subparsers(dest="command")

    info_parser = subparsers.add_parser("info", help=COMMANDS["info"]["desc"])
    info_parser.add_argument("path", type=Path, help="docs directory")
    info_parser.add_argument("--json", action="store_true", help="output as JSON")
    info_parser.add_argument("--ignore", action="append", default=[], help="ignore file pattern for inline refs")

    affected_parser = subparsers.add_parser("affected", help=COMMANDS["affected"]["desc"])
    affected_parser.add_argument("path", type=Path, help="docs directory")
    scope_group = affected_parser.add_mutually_exclusive_group(required=True)
    scope_group.add_argument("--since-base", action="store_true", help="compare from base in doctrace.json")
    scope_group.add_argument("--last", type=int, help="compare against HEAD~N (N must be > 0)")
    scope_group.add_argument("--base-branch", help="compare from merge-base(HEAD, <branch>)")
    scope_group.add_argument("--since", help="compare from git ref (commit/tag/branch)")
    affected_parser.add_argument("--json", action="store_true", help="output as JSON")
    affected_parser.add_argument("--ignore", action="append", default=[], help="ignore file pattern")

    preview_parser = subparsers.add_parser("preview", help=COMMANDS["preview"]["desc"])
    preview_parser.add_argument("path", type=Path, help="docs directory")
    preview_parser.add_argument("--port", type=int, default=DEFAULT_PREVIEW_PORT, help="server port")

    base_parser = subparsers.add_parser("base", help=COMMANDS["base"]["desc"])
    base_subparsers = base_parser.add_subparsers(dest="base_command", required=True)
    base_subparsers.add_parser("update", help="save current commit to doctrace.json")
    base_subparsers.add_parser("show", help="show base state")

    subparsers.add_parser("init", help=COMMANDS["init"]["desc"])

    index_parser = subparsers.add_parser("index", help=COMMANDS["index"]["desc"])
    index_parser.add_argument("path", type=Path, help="docs directory")
    index_parser.add_argument("-o", "--output", type=Path, required=True, help="output file")

    completion_parser = subparsers.add_parser("completion", help=COMMANDS["completion"]["desc"])
    completion_parser.add_argument("shell", nargs="?", help="shell type (zsh, bash, fish)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "info":
        sys.exit(info.run(args.path, args.json, args.ignore))
    elif args.command == "affected":
        sys.exit(
            affected.run(
                args.path,
                args.since_base,
                args.last,
                args.base_branch,
                args.since,
                args.json,
                args.ignore,
            )
        )
    elif args.command == "preview":
        sys.exit(preview.run(args.path, args.port))
    elif args.command == "base":
        if args.base_command == "update":
            sys.exit(base.run_update())
        elif args.base_command == "show":
            sys.exit(base.run_show())
    elif args.command == "init":
        sys.exit(init.run())
    elif args.command == "index":
        sys.exit(index.run(args.path, args.output))
    elif args.command == "completion":
        sys.exit(completion.run(args.shell))


if __name__ == "__main__":
    main()
