from pathlib import Path

from doctrack.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_preserves_line_numbers():
    result = parse_doc(INPUT)
    assert result.related_docs[0].line_number == 10
    assert result.related_sources[0].line_number == 13
