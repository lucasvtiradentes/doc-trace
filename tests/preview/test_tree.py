import tempfile
from pathlib import Path

from docsync.commands.preview.tree import _compute_levels, build_dependency_tree
from docsync.core.config import Config


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


def test_build_dependency_tree_independent():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "a.md", related_sources=["src/a.py"])
        _create_doc(docs_dir / "b.md", related_sources=["src/b.py"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 1
        assert len(tree.levels[0]) == 2
        assert tree.circular == []


def test_build_dependency_tree_with_deps():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "base.md", related_sources=["src/base.py"])
        _create_doc(docs_dir / "child.md", related_docs=["docs/base.md"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 2
        level_0_names = [p.name for p in tree.levels[0]]
        level_1_names = [p.name for p in tree.levels[1]]
        assert "base.md" in level_0_names
        assert "child.md" in level_1_names


def test_build_dependency_tree_multi_level():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "l0.md", related_sources=["src/l0.py"])
        _create_doc(docs_dir / "l1.md", related_docs=["docs/l0.md"])
        _create_doc(docs_dir / "l2.md", related_docs=["docs/l1.md"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 3


def test_build_dependency_tree_circular():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "a.md", related_docs=["docs/b.md"])
        _create_doc(docs_dir / "b.md", related_docs=["docs/a.md"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.circular) > 0


def test_compute_levels_empty():
    levels, circular = _compute_levels({})
    assert levels == [[]]
    assert circular == []


def test_compute_levels_single_doc():
    doc = Path("/docs/a.md")
    levels, circular = _compute_levels({doc: []})
    assert len(levels) == 1
    assert doc in levels[0]
    assert circular == []
