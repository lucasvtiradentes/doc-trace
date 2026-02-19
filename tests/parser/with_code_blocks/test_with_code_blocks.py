from pathlib import Path

from doctrace.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_ignores_code_blocks():
    result = parse_doc(INPUT)
    assert len(result.required_docs) == 1
    assert result.required_docs[0].path == "docs/real.md"
    assert len(result.sources) == 1
    assert result.sources[0].path == "src/real.py"
