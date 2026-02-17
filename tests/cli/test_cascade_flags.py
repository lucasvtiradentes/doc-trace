from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from docsync.cli import main


def test_cascade_requires_scope_flag():
    with patch.object(sys, "argv", ["docsync", "cascade", "docs/"]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 2


def test_cascade_last_passes_arguments_to_run():
    with patch("docsync.cli.cascade.run", return_value=0) as run_mock:
        with patch.object(sys, "argv", ["docsync", "cascade", "docs/", "--last", "5", "--show-changed-files"]):
            with pytest.raises(SystemExit) as exc:
                main()
    assert exc.value.code == 0
    run_mock.assert_called_once_with(Path("docs"), False, 5, None, True)
