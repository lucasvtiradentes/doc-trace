from docsync.core.config import validate_config


def test_validate_config_unknown_key():
    errors = validate_config({"unknown_key": "value"})
    assert len(errors) == 1
    assert "unknown key" in errors[0]


def test_validate_config_invalid_ignored_paths():
    errors = validate_config({"ignored_paths": "not_a_list"})
    assert len(errors) == 1
    assert "must be a list" in errors[0]


def test_validate_config_invalid_cascade_depth():
    errors = validate_config({"cascade_depth_limit": "not_an_int"})
    assert len(errors) == 1
    assert "must be null or integer" in errors[0]


def test_validate_config_invalid_metadata_style():
    errors = validate_config({"metadata": {"style": "invalid"}})
    assert len(errors) == 1
    assert "frontmatter" in errors[0]
