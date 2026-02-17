import re
from pathlib import Path
from typing import NamedTuple

RELATED_DOCS_HEADER = re.compile(r"^related docs:\s*$", re.MULTILINE | re.IGNORECASE)
RELATED_SOURCES_HEADER = re.compile(r"^related sources:\s*$", re.MULTILINE | re.IGNORECASE)
LIST_ITEM = re.compile(r"^-\s+(\S+(?:\s+\S+)*?)\s+-\s+(.+)$")


class RefEntry(NamedTuple):
    path: str
    description: str
    line_number: int


class ParsedDoc(NamedTuple):
    related_docs: list[RefEntry]
    related_sources: list[RefEntry]


def parse_doc(filepath: Path) -> ParsedDoc:
    content = filepath.read_text()
    lines = content.splitlines()
    related_docs = _extract_section(lines, RELATED_DOCS_HEADER)
    related_sources = _extract_section(lines, RELATED_SOURCES_HEADER)
    return ParsedDoc(related_docs=related_docs, related_sources=related_sources)


def _extract_section(lines: list[str], header_pattern: re.Pattern) -> list[RefEntry]:
    entries = []
    in_section = False
    for i, line in enumerate(lines, start=1):
        if header_pattern.match(line):
            in_section = True
            continue
        if in_section:
            if not line.strip():
                continue
            if line.startswith("-"):
                match = LIST_ITEM.match(line)
                if match:
                    entries.append(
                        RefEntry(path=match.group(1).strip(), description=match.group(2).strip(), line_number=i)
                    )
            else:
                break
    return entries
