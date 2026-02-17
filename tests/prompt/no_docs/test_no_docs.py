import tempfile
from pathlib import Path

from docsync.commands.prompt import generate_prompt
from docsync.core.config import Config


def test_prompt_no_docs():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        (tmppath / ".git").mkdir()
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        config = Config({})
        prompt = generate_prompt(docs_dir, config)
        assert "No docs found" in prompt
