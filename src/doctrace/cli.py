import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from doctrace.commands import affected, init, lock, preview, validate

VERSION = version("doctrace")


def main():
    parser = argparse.ArgumentParser(description="Keep docs in sync with code")
    parser.add_argument("-v", "--version", action="version", version=f"doctrace {VERSION}")
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="validate all refs exist")
    validate_parser.add_argument("path", type=Path, help="docs directory to validate")

    affected_parser = subparsers.add_parser("affected", help="list docs affected by git diff")
    affected_parser.add_argument("path", type=Path, nargs="?", default=Path("docs"), help="docs directory")
    scope_group = affected_parser.add_mutually_exclusive_group(required=True)
    scope_group.add_argument("--since-lock", action="store_true", help="compare from lock.json last_analyzed_commit")
    scope_group.add_argument("--last", type=int, help="compare against HEAD~N (N must be > 0)")
    scope_group.add_argument("--base-branch", help="compare from merge-base(HEAD, <branch>)")
    scope_group.add_argument("--since", help="compare from git ref (commit/tag/branch)")
    affected_parser.add_argument("--verbose", "-V", action="store_true", help="show changed files and match details")
    affected_parser.add_argument("--json", action="store_true", help="output as JSON")

    preview_parser = subparsers.add_parser("preview", help="interactive docs explorer in browser")
    preview_parser.add_argument("path", type=Path, nargs="?", default=Path("docs"), help="docs directory")
    preview_parser.add_argument("--port", type=int, default=8420, help="server port (default: 8420)")

    lock_parser = subparsers.add_parser("lock", help="manage lock.json state")
    lock_subparsers = lock_parser.add_subparsers(dest="lock_command", required=True)
    lock_subparsers.add_parser("update", help="save current commit to lock.json")
    lock_subparsers.add_parser("show", help="show lock.json state")

    subparsers.add_parser("init", help="create .doctrace/ folder")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate":
        sys.exit(validate.run(args.path))
    elif args.command == "affected":
        sys.exit(
            affected.run(
                args.path,
                args.since_lock,
                args.last,
                args.base_branch,
                args.since,
                args.verbose,
                args.json,
            )
        )
    elif args.command == "preview":
        sys.exit(preview.run(args.path, args.port))
    elif args.command == "lock":
        if args.lock_command == "update":
            sys.exit(lock.run_update())
        elif args.lock_command == "show":
            sys.exit(lock.run_show())
    elif args.command == "init":
        sys.exit(init.run())


if __name__ == "__main__":
    main()
