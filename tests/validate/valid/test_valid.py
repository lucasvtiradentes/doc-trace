import shutil
import tempfile
from pathlib import Path

from docsync.commands.validate import validate_refs
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_validate_refs_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        src_dir = tmppath / "src"
        src_dir.mkdir()
        (src_dir / "module.py").write_text("# module")
        config = Config({})
        results = list(validate_refs(docs_dir, config, repo_root=tmppath))
        assert len(results) == 1
        assert results[0].ok
