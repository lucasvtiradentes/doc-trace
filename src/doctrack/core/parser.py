from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from doctrack.core.config import MetadataConfig

LIST_ITEM = re.compile(r"^-\s+(\S+(?:\s+\S+)*?)\s+-\s+(.+)$")
LIST_ITEM_SIMPLE = re.compile(r"^\s*-\s+(\S+)(?:\s+-\s+(.+))?$")


class RefEntry(NamedTuple):
    path: str
    description: str
    line_number: int


class ParsedDoc(NamedTuple):
    related_docs: list[RefEntry]
    related_sources: list[RefEntry]


def parse_doc(filepath: Path, metadata_config: MetadataConfig | None = None) -> ParsedDoc:
    from doctrack.core.config import MetadataConfig

    if metadata_config is None:
        metadata_config = MetadataConfig({})

    content = filepath.read_text()
    lines = content.splitlines()

    if metadata_config.style == "frontmatter":
        metadata_lines = _get_frontmatter_section(lines)
    else:
        metadata_lines = _get_custom_section(lines, metadata_config.require_separator)

    docs_pattern = re.compile(rf"^{re.escape(metadata_config.docs_key)}:\s*$", re.IGNORECASE)
    sources_pattern = re.compile(rf"^{re.escape(metadata_config.sources_key)}:\s*$", re.IGNORECASE)

    related_docs = _extract_section(metadata_lines, docs_pattern, metadata_config.style)
    related_sources = _extract_section(metadata_lines, sources_pattern, metadata_config.style)
    return ParsedDoc(related_docs=related_docs, related_sources=related_sources)


def _get_frontmatter_section(lines: list[str]) -> list[tuple[int, str]]:
    if not lines or lines[0].strip() != "---":
        return []
    end_line = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_line = i
            break
    if end_line is None:
        return []
    return [(i + 1, line) for i, line in enumerate(lines) if 0 < i < end_line]


def _get_custom_section(lines: list[str], require_separator: bool) -> list[tuple[int, str]]:
    if not require_separator:
        return _filter_code_blocks(lines)

    in_code_block = False
    separator_line = None
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if line.strip() == "---":
            separator_line = i
    if separator_line is None:
        return []
    return [(i + 1, line) for i, line in enumerate(lines) if i > separator_line]


def _filter_code_blocks(lines: list[str]) -> list[tuple[int, str]]:
    result = []
    in_code_block = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            result.append((i + 1, line))
    return result


def _extract_section(lines: list[tuple[int, str]], header_pattern: re.Pattern, style: str) -> list[RefEntry]:
    entries = []
    in_section = False
    item_pattern = LIST_ITEM_SIMPLE if style == "frontmatter" else LIST_ITEM
    for line_num, line in lines:
        if header_pattern.match(line):
            in_section = True
            continue
        if in_section:
            if not line.strip():
                continue
            if line.strip().startswith("-"):
                match = item_pattern.match(line)
                if match:
                    path = match.group(1).strip()
                    desc = match.group(2).strip() if match.group(2) else ""
                    entries.append(RefEntry(path=path, description=desc, line_number=line_num))
            else:
                break
    return entries
