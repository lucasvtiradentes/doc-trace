from pathlib import Path

from doctrace.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_with_both_sections():
    result = parse_doc(INPUT)
    assert len(result.related_docs) == 1
    assert result.related_docs[0].path == "docs/other.md"
    assert result.related_docs[0].description == "related documentation"
    assert len(result.related_sources) == 2
    assert result.related_sources[0].path == "src/module.py"
    assert result.related_sources[1].path == "src/utils.py"
