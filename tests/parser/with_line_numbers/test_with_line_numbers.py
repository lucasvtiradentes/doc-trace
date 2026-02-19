from pathlib import Path

from doctrace.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_preserves_line_numbers():
    result = parse_doc(INPUT)
    assert result.required_docs[0].line_number == 3
    assert result.sources[0].line_number == 5
