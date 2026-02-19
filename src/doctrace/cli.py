import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from doctrace.commands import affected, base, init, preview, validate
from doctrace.core.constants import DEFAULT_PREVIEW_PORT

VERSION = version("doctrace")


def main():
    parser = argparse.ArgumentParser(description="Keep docs in sync with code")
    parser.add_argument("-v", "--version", action="version", version=f"doctrace {VERSION}")
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="validate all refs exist")
    validate_parser.add_argument("path", type=Path, help="docs directory to validate")
    validate_parser.add_argument("--phases", action="store_true", help="show docs organized by dependency phases")

    affected_parser = subparsers.add_parser("affected", help="list docs affected by git diff")
    affected_parser.add_argument("path", type=Path, help="docs directory")
    scope_group = affected_parser.add_mutually_exclusive_group(required=True)
    scope_group.add_argument("--since-base", action="store_true", help="compare from base in doctrace.json")
    scope_group.add_argument("--last", type=int, help="compare against HEAD~N (N must be > 0)")
    scope_group.add_argument("--base-branch", help="compare from merge-base(HEAD, <branch>)")
    scope_group.add_argument("--since", help="compare from git ref (commit/tag/branch)")
    affected_parser.add_argument("--verbose", "-V", action="store_true", help="show changed files and match details")
    affected_parser.add_argument("--json", action="store_true", help="output as JSON")

    preview_parser = subparsers.add_parser("preview", help="interactive docs explorer in browser")
    preview_parser.add_argument("path", type=Path, help="docs directory")
    preview_parser.add_argument("--port", type=int, default=DEFAULT_PREVIEW_PORT, help="server port")

    base_parser = subparsers.add_parser("base", help="manage base commit state")
    base_subparsers = base_parser.add_subparsers(dest="base_command", required=True)
    base_subparsers.add_parser("update", help="save current commit to doctrace.json")
    base_subparsers.add_parser("show", help="show base state")

    subparsers.add_parser("init", help="create doctrace.json")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate":
        sys.exit(validate.run(args.path, args.phases))
    elif args.command == "affected":
        sys.exit(
            affected.run(
                args.path,
                args.since_base,
                args.last,
                args.base_branch,
                args.since,
                args.verbose,
                args.json,
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


if __name__ == "__main__":
    main()
