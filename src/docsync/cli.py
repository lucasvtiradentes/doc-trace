import argparse
import sys
from pathlib import Path

from docsync.commands import cascade, check, init, sync, tree


def main():
    parser = argparse.ArgumentParser(description="Keep docs in sync with code")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="validate all refs exist")
    check_parser.add_argument("path", type=Path, help="docs directory to check")

    cascade_parser = subparsers.add_parser("cascade", help="list docs affected by git diff")
    cascade_parser.add_argument("commit", help="commit ref (e.g., HEAD~1, abc123)")
    cascade_parser.add_argument("--docs", type=Path, default=Path("docs"), help="docs directory")

    sync_parser = subparsers.add_parser("sync", help="generate prompt for AI to fix docs")
    sync_parser.add_argument("path", type=Path, help="docs directory")
    sync_parser.add_argument("--incremental", action="store_true", help="only include changed docs")
    sync_parser.add_argument("--json", action="store_true", help="output as JSON instead of text")
    sync_parser.add_argument("--parallel", action="store_true", help="ignore dependencies, sync all at once")

    tree_parser = subparsers.add_parser("tree", help="show doc dependency tree")
    tree_parser.add_argument("path", type=Path, help="docs directory")

    subparsers.add_parser("init", help="create .docsync/ folder")

    args = parser.parse_args()

    if args.command == "check":
        sys.exit(check.run(args.path))
    elif args.command == "cascade":
        sys.exit(cascade.run(args.commit, args.docs))
    elif args.command == "sync":
        sys.exit(sync.run(args.path, args.incremental, args.json, args.parallel))
    elif args.command == "tree":
        sys.exit(tree.run(args.path))
    elif args.command == "init":
        sys.exit(init.run())


if __name__ == "__main__":
    main()
