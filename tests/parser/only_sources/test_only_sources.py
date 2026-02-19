from pathlib import Path

from doctrace.core.docs import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_only_sources():
    result = parse_doc(INPUT)
    assert len(result.required_docs) == 0
    assert len(result.sources) == 1
    assert result.sources[0].path == "src/main.py"
