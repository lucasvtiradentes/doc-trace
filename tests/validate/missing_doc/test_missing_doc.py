import shutil
import tempfile
from pathlib import Path

from doctrace.commands.info import validate_refs
from doctrace.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_validate_refs_missing_doc():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        results = list(validate_refs(docs_dir, config, repo_root=tmppath))
        assert len(results) == 1
        assert not results[0].ok
        assert "not found" in results[0].errors[0].message
