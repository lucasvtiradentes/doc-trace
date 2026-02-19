import tempfile
from pathlib import Path

from doctrace.core.config import Config
from doctrace.core.docs import build_dependency_tree, compute_levels


def _create_doc(path: Path, required_docs: list[str] = None, sources: list[str] = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "---\n"
    if required_docs:
        content += "required_docs:\n"
        for doc in required_docs:
            content += f"  - {doc}: desc\n"
    if sources:
        content += "sources:\n"
        for src in sources:
            content += f"  - {src}: desc\n"
    content += "---\n\n# Test\n"
    path.write_text(content)


def test_build_dependency_tree_independent():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "a.md", sources=["src/a.py"])
        _create_doc(docs_dir / "b.md", sources=["src/b.py"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 1
        assert len(tree.levels[0]) == 2
        assert tree.circular == []


def test_build_dependency_tree_with_deps():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "base.md", sources=["src/base.py"])
        _create_doc(docs_dir / "child.md", required_docs=["docs/base.md"])
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
        _create_doc(docs_dir / "l0.md", sources=["src/l0.py"])
        _create_doc(docs_dir / "l1.md", required_docs=["docs/l0.md"])
        _create_doc(docs_dir / "l2.md", required_docs=["docs/l1.md"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 3


def test_build_dependency_tree_circular():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        _create_doc(docs_dir / "a.md", required_docs=["docs/b.md"])
        _create_doc(docs_dir / "b.md", required_docs=["docs/a.md"])
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.circular) > 0


def test_compute_levels_empty():
    result = compute_levels({})
    assert result.levels == [[]]
    assert result.circular == []


def test_compute_levels_single_doc():
    doc = Path("/docs/a.md")
    result = compute_levels({doc: []})
    assert len(result.levels) == 1
    assert doc in result.levels[0]
    assert result.circular == []
