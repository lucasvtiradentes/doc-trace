from __future__ import annotations

from pathlib import Path

from doctrace.core.config import find_repo_root, load_config
from doctrace.core.docs import build_doc_index

INDEX_MARKER = "## Documentation Index"
TOP_LEVEL_CATEGORY = "Top-Level"


def run(docs_path: Path, output_path: Path) -> int:
    config = load_config()
    repo_root = find_repo_root(docs_path)
    docs_path = docs_path.resolve()
    index = build_doc_index(docs_path, config, repo_root)

    rows = _build_rows(index, docs_path, repo_root)
    table = _render_table(rows)

    _write_index(output_path, table)
    print(f"Index written to {output_path}")
    return 0


def _build_rows(index, docs_path: Path, repo_root: Path) -> list[dict]:
    rows = []
    for doc_path, parsed in index.parsed_cache.items():
        if doc_path.name == "index.md":
            continue
        rel_path = doc_path.relative_to(repo_root)
        docs_rel = doc_path.relative_to(docs_path)
        parts = docs_rel.parts

        if len(parts) == 1:
            category = TOP_LEVEL_CATEGORY
        else:
            category = "/".join(parts[:-1])

        sort_cat = "" if category == TOP_LEVEL_CATEGORY else category.lower()
        rows.append(
            {
                "category": category,
                "file": str(rel_path),
                "description": parsed.description or parsed.title or docs_rel.stem,
                "related": len(parsed.related_docs),
                "required": len(parsed.required_docs),
                "sources": len(parsed.sources),
                "sort_key": (sort_cat, str(rel_path).lower()),
            }
        )

    rows.sort(key=lambda r: r["sort_key"])
    return rows


def _render_table(rows: list[dict]) -> str:
    if not rows:
        return "## Documentation Index\n\nNo documentation files found.\n"

    max_cat = max(len(r["category"]) for r in rows)
    max_file = max(len(r["file"]) for r in rows)
    max_desc = max(len(r["description"]) for r in rows)

    max_cat = max(max_cat, len("Category"))
    max_file = max(max_file, len("File"))
    max_desc = max(max_desc, len("Description"))

    cat_h = "Category".ljust(max_cat)
    file_h = "File".ljust(max_file)
    desc_h = "Description".ljust(max_desc)
    header = f"| {cat_h} | {file_h} | {desc_h} | Rel. docs | Req. docs | Sources |"
    sep = f"|{'-' * (max_cat + 2)}|{'-' * (max_file + 2)}|{'-' * (max_desc + 2)}|-----------|-----------|---------|"

    lines = [INDEX_MARKER, "", header, sep]

    current_cat = None
    for row in rows:
        if row["category"] != current_cat:
            if current_cat is not None:
                lines.append(sep)
            current_cat = row["category"]
            cat_display = row["category"]
        else:
            cat_display = ""

        line = (
            f"| {cat_display.ljust(max_cat)} "
            f"| {row['file'].ljust(max_file)} "
            f"| {row['description'].ljust(max_desc)} "
            f"| {str(row['related']).center(9)} "
            f"| {str(row['required']).center(9)} "
            f"| {str(row['sources']).center(7)} |"
        )
        lines.append(line)

    lines.append("")
    return "\n".join(lines)


def _write_index(target: Path, table: str) -> None:
    try:
        content = target.read_text(encoding="utf-8")
        if INDEX_MARKER in content:
            before = content.split(INDEX_MARKER)[0].rstrip()
            new_content = f"{before}\n\n{table}" if before else table
        else:
            new_content = f"{content.rstrip()}\n\n{table}"
    except FileNotFoundError:
        new_content = f"# Documentation\n\n{table}"

    target.write_text(new_content, encoding="utf-8")
