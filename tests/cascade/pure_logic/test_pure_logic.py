import tempfile
from pathlib import Path
from unittest.mock import patch

from docsync.commands.cascade import _cascade, _find_direct_hits, find_affected_docs
from docsync.core.config import Config


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
        with patch("docsync.commands.cascade._get_changed_files", return_value=[]):
            result = find_affected_docs(docs_dir, "HEAD~1", config, repo_root=tmppath)
        assert len(result.affected_docs) == 0


def test_find_direct_hits_exact_match():
    doc1 = Path("/docs/doc1.md")
    source_to_docs = {"src/module.py": [doc1]}
    hits = _find_direct_hits(["src/module.py"], source_to_docs)
    assert doc1 in hits


def test_find_direct_hits_directory_match():
    doc1 = Path("/docs/doc1.md")
    source_to_docs = {"src/booking/": [doc1]}
    hits = _find_direct_hits(["src/booking/booking.module.ts"], source_to_docs)
    assert doc1 in hits


def test_find_direct_hits_directory_no_match_without_slash():
    doc1 = Path("/docs/doc1.md")
    source_to_docs = {"src/booking": [doc1]}
    hits = _find_direct_hits(["src/booking/booking.module.ts"], source_to_docs)
    assert doc1 not in hits


def test_find_direct_hits_nested_directory():
    doc1 = Path("/docs/doc1.md")
    source_to_docs = {"api/src/booking/": [doc1]}
    hits = _find_direct_hits(["api/src/booking/commands/handler.ts"], source_to_docs)
    assert doc1 in hits
