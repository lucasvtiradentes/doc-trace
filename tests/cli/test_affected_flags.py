from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from doctrack.cli import main


def test_affected_requires_scope_flag():
    with patch.object(sys, "argv", ["doctrack", "affected", "docs/"]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 2


def test_affected_last_passes_arguments_to_run():
    with patch("doctrack.cli.affected.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["doctrack", "affected", "docs/", "--last", "5", "--verbose"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, 5, None, None, True, False)


def test_affected_json_flag():
    with patch("doctrack.cli.affected.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["doctrack", "affected", "docs/", "--last", "1", "--json"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, 1, None, None, False, True)


def test_affected_since_flag():
    with patch("doctrack.cli.affected.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["doctrack", "affected", "docs/", "--since", "v1.0.0"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, None, None, "v1.0.0", False, False)
