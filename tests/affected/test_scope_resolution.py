from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from doctrace.commands.affected import resolve_commit_ref
from doctrace.core.config import Config


def test_resolve_commit_ref_with_last():
    commit_ref = resolve_commit_ref(Path("."), last=5)
    assert commit_ref == "HEAD~5"


def test_resolve_commit_ref_last_must_be_positive():
    with pytest.raises(ValueError, match="--last must be greater than 0"):
        resolve_commit_ref(Path("."), last=0)


def test_resolve_commit_ref_with_since_base():
    mock_config = Config({"base": {"commit_hash": "abc123"}})
    with patch("doctrace.commands.affected.load_config", return_value=mock_config):
        commit_ref = resolve_commit_ref(Path("."), since_base=True)
    assert commit_ref == "abc123"


def test_resolve_commit_ref_since_base_missing_commit():
    mock_config = Config({})
    with patch("doctrace.commands.affected.load_config", return_value=mock_config):
        with pytest.raises(ValueError, match="doctrace.json has no base"):
            resolve_commit_ref(Path("."), since_base=True)


def test_resolve_commit_ref_with_base_branch():
    with patch("doctrace.commands.affected.get_merge_base", return_value="deadbeef") as mock:
        commit_ref = resolve_commit_ref(Path("/repo"), base_branch="main")
    assert commit_ref == "deadbeef"
    mock.assert_called_once()


def test_resolve_commit_ref_requires_exactly_one_option():
    with pytest.raises(ValueError, match="choose exactly one scope"):
        resolve_commit_ref(Path("."))


def test_resolve_commit_ref_with_since():
    commit_ref = resolve_commit_ref(Path("."), since="v1.0.0")
    assert commit_ref == "v1.0.0"


def test_resolve_commit_ref_with_since_commit_hash():
    commit_ref = resolve_commit_ref(Path("."), since="abc123def")
    assert commit_ref == "abc123def"


def test_resolve_commit_ref_with_since_branch():
    commit_ref = resolve_commit_ref(Path("."), since="feature/my-branch")
    assert commit_ref == "feature/my-branch"
