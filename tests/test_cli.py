"""CLI stub: until M2 ships checks, the command must not look like a pass."""

import pytest

from caxgauge import cli


def test_main_exits_non_zero_until_checks_exist(capsys: pytest.CaptureFixture[str]):
    assert cli.main() != 0
    err = capsys.readouterr().err
    assert "M2" in err
    assert "verified" not in err.lower()
