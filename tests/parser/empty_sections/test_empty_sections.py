from pathlib import Path

from doctrace.core.docs import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_empty_sections():
    result = parse_doc(INPUT)
    assert len(result.required_docs) == 0
    assert len(result.related_docs) == 0
    assert len(result.sources) == 0
