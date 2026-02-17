import tempfile
from pathlib import Path

from docsync.parser import parse_doc


def test_parse_doc_with_both_sections():
    content = """# Test Doc

Some content here.

---

related docs:
- docs/other.md - related documentation

related sources:
- src/module.py - implementation
- src/utils.py  - utilities
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_doc(Path(f.name))

    assert len(result.related_docs) == 1
    assert result.related_docs[0].path == "docs/other.md"
    assert result.related_docs[0].description == "related documentation"

    assert len(result.related_sources) == 2
    assert result.related_sources[0].path == "src/module.py"
    assert result.related_sources[1].path == "src/utils.py"


def test_parse_doc_empty_sections():
    content = """# Test Doc

No related sections here.
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_doc(Path(f.name))

    assert len(result.related_docs) == 0
    assert len(result.related_sources) == 0


def test_parse_doc_only_sources():
    content = """# Test Doc

related sources:
- src/main.py - entry point
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_doc(Path(f.name))

    assert len(result.related_docs) == 0
    assert len(result.related_sources) == 1
    assert result.related_sources[0].path == "src/main.py"


def test_parse_doc_preserves_line_numbers():
    content = """# Test Doc

Line 2
Line 3
Line 4

related docs:
- docs/a.md - doc a

related sources:
- src/b.py - source b
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_doc(Path(f.name))

    assert result.related_docs[0].line_number == 8
    assert result.related_sources[0].line_number == 11
