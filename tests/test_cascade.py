import tempfile
from pathlib import Path
from unittest.mock import patch

from docsync.cascade import _build_indexes, _cascade, find_affected_docs
from docsync.config import Config


def test_build_indexes():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        doc1 = docs_dir / "doc1.md"
        doc1.write_text("""# Doc1

related docs:
- docs/doc2.md - related

related sources:
- src/module.py - impl
""")
        doc2 = docs_dir / "doc2.md"
        doc2.write_text("""# Doc2

related sources:
- src/other.py - other
""")
        source_to_docs, doc_to_docs = _build_indexes(docs_dir, tmppath)
        assert "src/module.py" in source_to_docs
        assert "src/other.py" in source_to_docs
        assert len(source_to_docs["src/module.py"]) == 1


def test_cascade_no_depth_limit():
    doc1 = Path("/docs/doc1.md")
    doc2 = Path("/docs/doc2.md")
    doc3 = Path("/docs/doc3.md")
    doc_to_docs = {
        doc1: [doc2],
        doc2: [doc3],
    }
    cascade_hits, circular = _cascade([doc1], doc_to_docs, depth_limit=None)
    assert doc2 in cascade_hits
    assert doc3 in cascade_hits


def test_cascade_with_depth_limit():
    doc1 = Path("/docs/doc1.md")
    doc2 = Path("/docs/doc2.md")
    doc3 = Path("/docs/doc3.md")
    doc_to_docs = {
        doc1: [doc2],
        doc2: [doc3],
    }
    cascade_hits, circular = _cascade([doc1], doc_to_docs, depth_limit=1)
    assert doc2 in cascade_hits
    assert doc3 not in cascade_hits


def test_cascade_detects_circular():
    doc1 = Path("/docs/doc1.md")
    doc2 = Path("/docs/doc2.md")
    doc3 = Path("/docs/doc3.md")
    doc_to_docs = {
        doc1: [doc2],
        doc2: [doc3],
        doc3: [doc2],
    }
    cascade_hits, circular = _cascade([doc1], doc_to_docs, depth_limit=None)
    assert len(circular) > 0
    assert (doc3, doc2) in circular


def test_find_affected_docs_no_changes():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        config = Config({})
        with patch("docsync.cascade._get_changed_files", return_value=[]):
            result = find_affected_docs(docs_dir, "HEAD~1", config, repo_root=tmppath)
        assert len(result.affected_docs) == 0


def test_find_affected_docs_with_changes():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        doc = docs_dir / "test.md"
        doc.write_text("""# Test

related sources:
- src/changed.py - impl
""")
        config = Config({})
        with patch("docsync.cascade._get_changed_files", return_value=["src/changed.py"]):
            result = find_affected_docs(docs_dir, "HEAD~1", config, repo_root=tmppath)
        assert len(result.direct_hits) == 1
        assert result.direct_hits[0] == doc
