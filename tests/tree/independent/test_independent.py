import shutil
import tempfile
from pathlib import Path

from docsync.commands.tree import build_dependency_tree
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_tree_independent_docs():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        tree = build_dependency_tree(docs_dir, config, tmppath)
        assert len(tree.levels) == 1
        assert len(tree.levels[0]) == 2
        assert tree.circular == []
