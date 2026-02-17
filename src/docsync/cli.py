import argparse
import sys
from pathlib import Path

from docsync.cascade import find_affected_docs
from docsync.config import init_config, load_config
from docsync.validator import check_refs, validate_docs


def main():
    parser = argparse.ArgumentParser(description="Auto-validate and update docs in large codebases")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="validate all refs exist")
    check_parser.add_argument("path", type=Path, help="docs directory to check")

    cascade_parser = subparsers.add_parser("cascade", help="list docs affected by git diff")
    cascade_parser.add_argument("commit", help="commit ref (e.g., HEAD~1, abc123)")
    cascade_parser.add_argument("--docs", type=Path, default=Path("docs"), help="docs directory")

    validate_parser = subparsers.add_parser("validate", help="run claude to validate doc content")
    validate_parser.add_argument("path", type=Path, help="docs directory to validate")
    validate_parser.add_argument("--incremental", action="store_true", help="only validate changed docs")

    subparsers.add_parser("init", help="create .docsync.json template")

    args = parser.parse_args()

    if args.command == "check":
        sys.exit(cmd_check(args.path))
    elif args.command == "cascade":
        sys.exit(cmd_cascade(args.commit, args.docs))
    elif args.command == "validate":
        sys.exit(cmd_validate(args.path, args.incremental))
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


def cmd_validate(docs_path: Path, incremental: bool) -> int:
    config = load_config()
    for output in validate_docs(docs_path, config, incremental):
        print(output)
    return 0


def cmd_init() -> int:
    config_path = init_config(Path.cwd())
    print(f"Created {config_path}")
    return 0


if __name__ == "__main__":
    main()
