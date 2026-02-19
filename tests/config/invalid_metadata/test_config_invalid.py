from doctrace.core.config import validate_config


def test_validate_config_unknown_key():
    errors = validate_config({"unknown_key": "value"})
    assert len(errors) == 1
    assert "unknown key" in errors[0]


def test_validate_config_invalid_metadata_unknown_key():
    errors = validate_config({"metadata": {"unknown_key": "value"}})
    assert len(errors) == 1
    assert "unknown key" in errors[0]
