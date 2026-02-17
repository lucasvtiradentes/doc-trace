import shutil
import tempfile
from pathlib import Path

from docsync.commands.prompt import generate_prompt
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_prompt_ordered():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        (tmppath / ".git").mkdir()
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        prompt = generate_prompt(docs_dir, config, incremental=False, parallel=False)
        assert "Phase 1" in prompt
        assert "Phase 2" in prompt
        assert "base.md" in prompt
        assert "child.md" in prompt
