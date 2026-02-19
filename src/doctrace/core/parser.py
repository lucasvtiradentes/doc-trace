from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from doctrace.core.config import MetadataConfig

LIST_ITEM_YAML = re.compile(r"^\s*-\s+([^:]+?):\s*(.*)$")


class RefEntry(NamedTuple):
    path: str
    description: str
    line_number: int


class ParsedDoc(NamedTuple):
    required_docs: list[RefEntry]
    related_docs: list[RefEntry]
    sources: list[RefEntry]


def parse_doc(filepath: Path, metadata_config: MetadataConfig | None = None) -> ParsedDoc:
    from doctrace.core.config import MetadataConfig

    if metadata_config is None:
        metadata_config = MetadataConfig({})

    content = filepath.read_text()
    lines = content.splitlines()
    metadata_lines = _get_frontmatter_section(lines)

    required_docs_pattern = re.compile(rf"^{re.escape(metadata_config.required_docs_key)}:\s*$", re.IGNORECASE)
    related_docs_pattern = re.compile(rf"^{re.escape(metadata_config.related_docs_key)}:\s*$", re.IGNORECASE)
    sources_pattern = re.compile(rf"^{re.escape(metadata_config.sources_key)}:\s*$", re.IGNORECASE)

    required_docs = _extract_section(metadata_lines, required_docs_pattern)
    related_docs = _extract_section(metadata_lines, related_docs_pattern)
    sources = _extract_section(metadata_lines, sources_pattern)
    return ParsedDoc(required_docs=required_docs, related_docs=related_docs, sources=sources)


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


def _extract_section(lines: list[tuple[int, str]], header_pattern: re.Pattern) -> list[RefEntry]:
    entries = []
    in_section = False
    for line_num, line in lines:
        if header_pattern.match(line):
            in_section = True
            continue
        if in_section:
            if not line.strip():
                continue
            if line.strip().startswith("-"):
                match = LIST_ITEM_YAML.match(line)
                if match:
                    path = match.group(1).strip()
                    desc = match.group(2).strip() if match.group(2) else ""
                    entries.append(RefEntry(path=path, description=desc, line_number=line_num))
            else:
                break
    return entries
