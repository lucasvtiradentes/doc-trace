import shutil
import tempfile
from pathlib import Path

from docsync.commands.tree import build_dependency_tree, format_tree
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_tree_with_dependencies():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 2
        level_0_names = [p.name for p in tree.levels[0]]
        level_1_names = [p.name for p in tree.levels[1]]
        assert "base.md" in level_0_names
        assert "child.md" in level_1_names


def test_format_tree_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        output = format_tree(tree, tmppath)
        assert "Level 0" in output
        assert "Level 1" in output
        assert "depends on:" in output
