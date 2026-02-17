from pathlib import Path

from doctrack.core.config import MetadataConfig
from doctrack.core.parser import parse_doc

INPUT = Path(__file__).parent / "input.md"


def test_parse_doc_frontmatter_style():
    config = MetadataConfig({"style": "frontmatter"})
    result = parse_doc(INPUT, config)
    assert len(result.related_docs) == 1
    assert result.related_docs[0].path == "docs/foo.md"
    assert len(result.related_sources) == 1
    assert result.related_sources[0].path == "src/bar.py"
