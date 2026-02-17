import tempfile
from pathlib import Path

from doctrace.commands.preview.graph import build_graph_data, generate_html
from doctrace.core.config import Config


def _create_doc(path: Path, related_docs: list[str] = None, related_sources: list[str] = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "# Test\n\n---\n\n"
    if related_docs:
        content += "related docs:\n"
        for doc in related_docs:
            content += f"- {doc} - desc\n"
        content += "\n"
    if related_sources:
        content += "related sources:\n"
        for src in related_sources:
            content += f"- {src} - desc\n"
    path.write_text(content)


def test_build_graph_data_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "a.md", related_sources=["src/a.py"])
        _create_doc(docs_dir / "b.md", related_docs=["docs/a.md"])
        config = Config({})
        data = build_graph_data(docs_dir, config, tmppath)
        assert "nodes" in data
        assert "edges" in data
        assert "levels" in data
        assert "stats" in data
        assert len(data["nodes"]) == 2
        assert len(data["edges"]) == 1


def test_build_graph_data_stats():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "a.md", related_sources=["src/a.py"])
        _create_doc(docs_dir / "b.md", related_sources=["src/b.py"])
        config = Config({})
        data = build_graph_data(docs_dir, config, tmppath)
        assert data["stats"]["total"] == 2
        assert data["stats"]["independent"] == 2
        assert data["stats"]["circular"] == 0


def test_build_graph_data_node_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "test.md", related_sources=["src/test.py"])
        config = Config({})
        data = build_graph_data(docs_dir, config, tmppath)
        node = data["nodes"][0]
        assert "id" in node
        assert "path" in node
        assert "name" in node
        assert "level" in node
        assert node["name"] == "test"


def test_generate_html_contains_graph_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "test.md", related_sources=["src/test.py"])
        config = Config({})
        data = build_graph_data(docs_dir, config, tmppath)
        html = generate_html(data)
        assert "<!DOCTYPE html>" in html
        assert '"nodes"' in html
        assert '"edges"' in html
