from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from docsync.commands.cascade import resolve_commit_ref
from docsync.core.lock import Lock


def test_resolve_commit_ref_with_last():
    commit_ref = resolve_commit_ref(Path("."), last=5)
    assert commit_ref == "HEAD~5"


def test_resolve_commit_ref_last_must_be_positive():
    with pytest.raises(ValueError, match="--last must be greater than 0"):
        resolve_commit_ref(Path("."), last=0)


def test_resolve_commit_ref_with_since_lock():
    with patch("docsync.commands.cascade.load_lock", return_value=Lock({"last_analyzed_commit": "abc123"})):
        commit_ref = resolve_commit_ref(Path("."), since_lock=True)
    assert commit_ref == "abc123"


def test_resolve_commit_ref_since_lock_missing_commit():
    with patch("docsync.commands.cascade.load_lock", return_value=Lock({})):
        with pytest.raises(ValueError, match="lock.json has no last_analyzed_commit"):
            resolve_commit_ref(Path("."), since_lock=True)


def test_resolve_commit_ref_with_base_branch():
    completed = subprocess.CompletedProcess(
        args=["git", "merge-base", "HEAD", "main"], returncode=0, stdout="deadbeef\n", stderr=""
    )
    with patch("docsync.commands.cascade.subprocess.run", return_value=completed) as run_mock:
        commit_ref = resolve_commit_ref(Path("/repo"), base_branch="main")
    assert commit_ref == "deadbeef"
    run_mock.assert_called_once()


def test_resolve_commit_ref_requires_exactly_one_option():
    with pytest.raises(ValueError, match="choose exactly one scope"):
        resolve_commit_ref(Path("."))
