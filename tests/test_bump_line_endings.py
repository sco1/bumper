from pathlib import Path

import pytest
from packaging.version import Version

from bumper.bump import BumpType, bump_ver
from bumper.config import BumperFile

LINE_ENDING_TEST_CASES = (
    pytest.param(b'[project]\nversion = "0.1.0"\n', id="lf"),
    pytest.param(b'[project]\r\nversion = "0.1.0"\r\n', id="crlf"),
    pytest.param(b'[project]\r\nversion = "0.1.0"\n# trailing\r\n', id="mixed"),
    pytest.param(b'[project]\nversion = "0.1.0"', id="no-trailing-newline"),
)


@pytest.mark.parametrize("src", LINE_ENDING_TEST_CASES)
def test_bump_preserves_line_endings(tmp_path: Path, src: bytes) -> None:
    target = tmp_path / "pyproject.toml"
    target.write_bytes(src)

    bump_ver(
        current_version=Version("0.1.0"),
        files=[BumperFile(file=target, search='version = "{current_version}"')],
        bump_type=BumpType.PATCH,
        dry_run=False,
    )

    truth_out = src.replace(b'version = "0.1.0"', b'version = "0.1.1"')
    assert target.read_bytes() == truth_out


@pytest.mark.parametrize("src", LINE_ENDING_TEST_CASES)
def test_dry_run_diff_ignores_line_endings(
    tmp_path: Path, src: bytes, capsys: pytest.CaptureFixture
) -> None:
    target = tmp_path / "pyproject.toml"
    target.write_bytes(src)

    bump_ver(
        current_version=Version("0.1.0"),
        files=[BumperFile(file=target, search='version = "{current_version}"')],
        bump_type=BumpType.PATCH,
        dry_run=True,
    )

    captured = capsys.readouterr()
    assert "\r" not in captured.out
    assert '-version = "0.1.0"\n+version = "0.1.1"' in captured.out
    assert target.read_bytes() == src
