import shutil
import tempfile
from pathlib import Path

from docsync.commands.prompt import generate_prompt
from docsync.core.config import Config

DOCS_DIR = Path(__file__).parent / "docs"


def test_prompt_parallel():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        (tmppath / ".git").mkdir()
        docs_dir = tmppath / "docs"
        shutil.copytree(DOCS_DIR, docs_dir)
        config = Config({})
        prompt = generate_prompt(docs_dir, config, incremental=False, parallel=True)
        assert "a.md" in prompt
        assert "b.md" in prompt
        assert "Phase" not in prompt
