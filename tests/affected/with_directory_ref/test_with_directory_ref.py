import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from docsync.commands.affected import find_affected_docs
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_find_affected_docs_with_directory_ref():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        with patch("docsync.commands.affected.get_changed_files", return_value=["api/src/booking/booking.module.ts"]):
            result = find_affected_docs(docs_dir, "HEAD~1", config, repo_root=tmppath)
        assert len(result.direct_hits) == 1
        assert result.direct_hits[0] == docs_dir / "bookings.md"
