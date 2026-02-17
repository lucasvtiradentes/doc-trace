import shutil
import tempfile
from pathlib import Path

from docsync.commands.affected import _build_indexes
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_build_indexes():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        source_to_docs, doc_to_docs = _build_indexes(docs_dir, tmppath, config)
        assert "src/module.py" in source_to_docs
        assert "src/other.py" in source_to_docs
        assert len(source_to_docs["src/module.py"]) == 1
