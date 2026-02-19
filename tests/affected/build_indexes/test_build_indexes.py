import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from doctrace.commands.affected import _get_doc_metadata
from doctrace.core.config import Config
from doctrace.core.docs import build_doc_index

DOCS_DIR = Path(__file__).parent / "docs"


def test_build_doc_index():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        index = build_doc_index(docs_dir, config, tmppath)
        assert "src/module.py" in index.source_to_docs
        assert "src/other.py" in index.source_to_docs
        assert len(index.source_to_docs["src/module.py"]) == 1
        assert len(index.parsed_cache) > 0


def test_get_doc_metadata_uses_cache():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        index = build_doc_index(docs_dir, config, tmppath)
        affected_docs = list(index.parsed_cache.keys())
        with patch("doctrace.commands.affected.parse_doc") as mock_parse:
            _get_doc_metadata(affected_docs, config, tmppath, index.parsed_cache)
            mock_parse.assert_not_called()
