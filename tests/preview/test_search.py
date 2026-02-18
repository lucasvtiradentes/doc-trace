import tempfile
from pathlib import Path

from doctrace.commands.preview.search import search_docs


def test_search_docs_finds_match():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "test.md").write_text("# Hello World\n\nThis is a test document.")
        results = search_docs(tmppath, docs_dir, "hello")
        assert len(results) == 1
        assert results[0]["name"] == "test"
        assert len(results[0]["matches"]) >= 1


def test_search_docs_no_match():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "test.md").write_text("# Foo\n\nBar baz.")
        results = search_docs(tmppath, docs_dir, "notfound")
        assert len(results) == 0


def test_search_docs_case_insensitive():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "test.md").write_text("# UPPERCASE content")
        results = search_docs(tmppath, docs_dir, "uppercase")
        assert len(results) == 1


def test_search_docs_multiple_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "a.md").write_text("# Doc A\n\nSearchterm here.")
        (docs_dir / "b.md").write_text("# Doc B\n\nNo match.")
        (docs_dir / "c.md").write_text("# Doc C\n\nAnother Searchterm.")
        results = search_docs(tmppath, docs_dir, "searchterm")
        assert len(results) == 2
        names = [r["name"] for r in results]
        assert "a" in names
        assert "c" in names


def test_search_docs_returns_line_numbers():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "test.md").write_text("Line 1\nLine 2\nKeyword here\nLine 4")
        results = search_docs(tmppath, docs_dir, "keyword")
        assert len(results) == 1
        assert results[0]["matches"][0]["line"] == 3
