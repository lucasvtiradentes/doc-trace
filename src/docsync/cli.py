import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from docsync.commands import cascade, check, init, prompt, tree

VERSION = version("docsync")


def main():
    parser = argparse.ArgumentParser(description="Keep docs in sync with code")
    parser.add_argument("-v", "--version", action="version", version=f"docsync {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="validate all refs exist")
    check_parser.add_argument("path", type=Path, help="docs directory to check")

    cascade_parser = subparsers.add_parser("cascade", help="list docs affected by git diff")
    cascade_parser.add_argument("commit", help="commit ref (e.g., HEAD~1, abc123)")
    cascade_parser.add_argument("--docs", type=Path, default=Path("docs"), help="docs directory")

    prompt_parser = subparsers.add_parser("prompt", help="generate prompt for AI to review docs")
    prompt_parser.add_argument("path", type=Path, help="docs directory")
    prompt_parser.add_argument("--incremental", action="store_true", help="only include changed docs")
    prompt_parser.add_argument("--parallel", action="store_true", help="ignore dependencies, all at once")
    prompt_parser.add_argument("--update-lock", action="store_true", help="update lock.json with current commit")

    tree_parser = subparsers.add_parser("tree", help="show doc dependency tree")
    tree_parser.add_argument("path", type=Path, help="docs directory")

    subparsers.add_parser("init", help="create .docsync/ folder")

    args = parser.parse_args()

    if args.command == "check":
        sys.exit(check.run(args.path))
    elif args.command == "cascade":
        sys.exit(cascade.run(args.commit, args.docs))
    elif args.command == "prompt":
        sys.exit(prompt.run(args.path, args.incremental, args.parallel, args.update_lock))
    elif args.command == "tree":
        sys.exit(tree.run(args.path))
    elif args.command == "init":
        sys.exit(init.run())


if __name__ == "__main__":
    main()
