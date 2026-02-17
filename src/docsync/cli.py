import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from docsync.commands import affected, init, lock, tree, validate

VERSION = version("docsync")


def main():
    parser = argparse.ArgumentParser(description="Keep docs in sync with code")
    parser.add_argument("-v", "--version", action="version", version=f"docsync {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate all refs exist")
    validate_parser.add_argument("path", type=Path, help="docs directory to validate")

    affected_parser = subparsers.add_parser("affected", help="list docs affected by git diff")
    affected_parser.add_argument("path", type=Path, nargs="?", default=Path("docs"), help="docs directory")
    scope_group = affected_parser.add_mutually_exclusive_group(required=True)
    scope_group.add_argument("--since-lock", action="store_true", help="compare from lock.json last_analyzed_commit")
    scope_group.add_argument("--last", type=int, help="compare against HEAD~N (N must be > 0)")
    scope_group.add_argument("--base-branch", help="compare from merge-base(HEAD, <branch>)")
    affected_parser.add_argument("--show-changed-files", action="store_true", help="print changed files before hits")
    output_group = affected_parser.add_mutually_exclusive_group()
    output_group.add_argument("--ordered", action="store_true", help="group output by dependency phases")
    output_group.add_argument("--parallel", action="store_true", help="flat list for parallel processing")

    tree_parser = subparsers.add_parser("tree", help="show doc dependency tree")
    tree_parser.add_argument("path", type=Path, help="docs directory")

    lock_parser = subparsers.add_parser("lock", help="manage lock.json state")
    lock_subparsers = lock_parser.add_subparsers(dest="lock_command", required=True)
    lock_subparsers.add_parser("update", help="save current commit to lock.json")
    lock_subparsers.add_parser("show", help="show lock.json state")

    subparsers.add_parser("init", help="create .docsync/ folder")

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(validate.run(args.path))
    elif args.command == "affected":
        sys.exit(affected.run(
            args.path, args.since_lock, args.last, args.base_branch,
            args.show_changed_files, args.ordered, args.parallel
        ))
    elif args.command == "tree":
        sys.exit(tree.run(args.path))
    elif args.command == "lock":
        if args.lock_command == "update":
            sys.exit(lock.run_update())
        elif args.lock_command == "show":
            sys.exit(lock.run_show())
    elif args.command == "init":
        sys.exit(init.run())


if __name__ == "__main__":
    main()
