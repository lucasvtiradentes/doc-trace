from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from docsync.cli import main


def test_affected_requires_scope_flag():
    with patch.object(sys, "argv", ["docsync", "affected", "docs/"]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 2


def test_affected_last_passes_arguments_to_run():
    with patch("docsync.cli.affected.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["docsync", "affected", "docs/", "--last", "5", "--show-changed-files"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, 5, None, True, False, False)


def test_affected_ordered_flag():
    with patch("docsync.cli.affected.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["docsync", "affected", "docs/", "--last", "1", "--ordered"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, 1, None, False, True, False)


def test_affected_parallel_flag():
    with patch("docsync.cli.affected.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["docsync", "affected", "docs/", "--last", "1", "--parallel"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, 1, None, False, False, True)
