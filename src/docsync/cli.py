import argparse
import sys
from pathlib import Path

from docsync.cascade import find_affected_docs
from docsync.config import init_docsync, load_config
from docsync.tree import build_dependency_tree, format_tree
from docsync.validator import _find_repo_root, check_refs, generate_sync_prompt, print_validation_report


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
        sys.exit(cmd_check(args.path))
    elif args.command == "cascade":
        sys.exit(cmd_cascade(args.commit, args.docs))
    elif args.command == "sync":
        sys.exit(cmd_sync(args.path, args.incremental, args.json, args.parallel))
    elif args.command == "tree":
        sys.exit(cmd_tree(args.path))
    elif args.command == "init":
        sys.exit(cmd_init())


def cmd_check(docs_path: Path) -> int:
    config = load_config()
    has_errors = False
    for result in check_refs(docs_path, config):
        if not result.ok:
            has_errors = True
            for error in result.errors:
                print(f"{result.doc_path}:{error.ref.line_number}: {error.message}")
    if has_errors:
        return 1
    print("All refs valid")
    return 0


def cmd_cascade(commit_ref: str, docs_path: Path) -> int:
    config = load_config()
    result = find_affected_docs(docs_path, commit_ref, config)
    if not result.affected_docs:
        print("No docs affected")
        return 0
    print(f"Direct hits ({len(result.direct_hits)}):")
    for doc in result.direct_hits:
        print(f"  {doc}")
    if result.cascade_hits:
        print(f"\nCascade hits ({len(result.cascade_hits)}):")
        for doc in result.cascade_hits:
            print(f"  {doc}")
    if result.circular_refs:
        print("\nWarning: circular refs detected:")
        for src, dst in result.circular_refs:
            print(f"  {src} <-> {dst}")
    return 0


def cmd_sync(docs_path: Path, incremental: bool, as_json: bool, parallel: bool) -> int:
    config = load_config()
    if as_json:
        print(print_validation_report(docs_path, config, incremental))
    else:
        print(generate_sync_prompt(docs_path, config, incremental, parallel))
    return 0


def cmd_tree(docs_path: Path) -> int:
    config = load_config()
    docs_path = docs_path.resolve()
    repo_root = _find_repo_root(docs_path)
    tree = build_dependency_tree(docs_path, config, repo_root)
    print(format_tree(tree, repo_root))
    return 0


def cmd_init() -> int:
    docsync_dir = init_docsync(Path.cwd())
    print(f"Created {docsync_dir}/")
    return 0


if __name__ == "__main__":
    main()
