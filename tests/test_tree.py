import tempfile
from pathlib import Path

from docsync.commands.tree import build_dependency_tree, format_tree
from docsync.core.config import Config


def test_tree_independent_docs():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "a.md").write_text("# A\n\nrelated sources:\n- src/a.py - a")
        (docs_dir / "b.md").write_text("# B\n\nrelated sources:\n- src/b.py - b")
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 1
        assert len(tree.levels[0]) == 2
        assert tree.circular == []


def test_tree_with_dependencies():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "base.md").write_text("# Base\n\nrelated sources:\n- src/base.py - base")
        (docs_dir / "child.md").write_text("# Child\n\nrelated docs:\n- docs/base.md - base")
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 2
        level_0_names = [p.name for p in tree.levels[0]]
        level_1_names = [p.name for p in tree.levels[1]]
        assert "base.md" in level_0_names
        assert "child.md" in level_1_names


def test_tree_multi_level():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "l0.md").write_text("# L0\n\nrelated sources:\n- src/l0.py - l0")
        (docs_dir / "l1.md").write_text("# L1\n\nrelated docs:\n- docs/l0.md - l0")
        (docs_dir / "l2.md").write_text("# L2\n\nrelated docs:\n- docs/l1.md - l1")
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 3


def test_tree_circular_deps():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "a.md").write_text("# A\n\nrelated docs:\n- docs/b.md - b")
        (docs_dir / "b.md").write_text("# B\n\nrelated docs:\n- docs/a.md - a")
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.circular) > 0


def test_format_tree_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "base.md").write_text("# Base\n\nrelated sources:\n- src/base.py - base")
        (docs_dir / "child.md").write_text("# Child\n\nrelated docs:\n- docs/base.md - base")
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        output = format_tree(tree, tmppath)
        assert "Level 0" in output
        assert "Level 1" in output
        assert "depends on:" in output
