from doctrace.core.config import validate_config


def test_validate_config_valid():
    errors = validate_config({"ignored_paths": ["*.md"], "affected_depth_limit": 2})
    assert errors == []


def test_validate_config_metadata():
    errors = validate_config(
        {"metadata": {"style": "frontmatter", "docs_key": "docs", "sources_key": "sources", "require_separator": False}}
    )
    assert errors == []
