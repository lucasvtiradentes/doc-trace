import shutil
import tempfile
from pathlib import Path

from doctrace.commands.info import find_undeclared_inline_refs
from doctrace.core.config import Config
from doctrace.core.docs import build_doc_index

DOCS_DIR = Path(__file__).parent / "docs"


def test_inline_refs_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir).resolve()
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        index = build_doc_index(docs_dir, config, repo_root=tmppath)
        undeclared = find_undeclared_inline_refs(index.parsed_cache, tmppath, "docs/", [])
        assert len(undeclared) == 0
