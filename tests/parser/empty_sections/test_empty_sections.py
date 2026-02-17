from pathlib import Path

from docsync.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_empty_sections():
    result = parse_doc(INPUT)
    assert len(result.related_docs) == 0
    assert len(result.related_sources) == 0
