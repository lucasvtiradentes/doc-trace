import shutil
import tempfile
from pathlib import Path

from doctrace.commands.info import find_missing_bidirectional
from doctrace.core.config import Config
from doctrace.core.docs import build_doc_index

DOCS_DIR = Path(__file__).parent / "docs"


def test_bidirectional_missing():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir).resolve()
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        index = build_doc_index(docs_dir, config, repo_root=tmppath)
        missing = find_missing_bidirectional(index.parsed_cache, tmppath)
        assert len(missing) == 1
        doc_a, doc_b = missing[0]
        assert "a.md" in str(doc_a)
        assert "b.md" in str(doc_b)
