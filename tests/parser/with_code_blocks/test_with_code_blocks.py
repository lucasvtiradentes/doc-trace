from pathlib import Path

from doctrace.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_ignores_code_blocks():
    result = parse_doc(INPUT)
    assert len(result.related_docs) == 1
    assert result.related_docs[0].path == "docs/real.md"
    assert len(result.related_sources) == 1
    assert result.related_sources[0].path == "src/real.py"
