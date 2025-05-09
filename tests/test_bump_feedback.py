from pathlib import Path

import pytest
from packaging.version import Version

from bumper.bump import BumpType, BumperFile, bump_ver


def test_empty_diff_feedback_single_file(dummy_repo: Path, capsys: pytest.CaptureFixture) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
    ]

    bump_ver(
        current_version=Version("100.200.300"),
        files=files,
        bump_type=BumpType.MAJOR,
        dry_run=False,
    )

    captured = capsys.readouterr()
    assert "pyproject.toml - No changes" in captured.out


def test_empty_diff_feedback_multi_file(dummy_repo: Path, capsys: pytest.CaptureFixture) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    readme = dummy_repo / "README.md"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
        BumperFile(file=readme, search="sco1-bumper/{current_version}"),
    ]

    bump_ver(
        current_version=Version("100.200.300"),
        files=files,
        bump_type=BumpType.MAJOR,
        dry_run=False,
    )

    captured = capsys.readouterr()
    assert "pyproject.toml - No changes" in captured.out
    assert "README.md - No changes" in captured.out


def test_bumped_feedback_single_file(dummy_repo: Path, capsys: pytest.CaptureFixture) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
    ]

    bump_ver(
        current_version=Version("0.1.0"),
        files=files,
        bump_type=BumpType.MAJOR,
        dry_run=False,
    )

    captured = capsys.readouterr()
    assert "Bumped pyproject.toml" in captured.out


def test_bumped_feedback_multi_file(dummy_repo: Path, capsys: pytest.CaptureFixture) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    readme = dummy_repo / "README.md"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
        BumperFile(file=readme, search="sco1-bumper/{current_version}"),
    ]

    bump_ver(
        current_version=Version("0.1.0"),
        files=files,
        bump_type=BumpType.MAJOR,
        dry_run=False,
    )

    captured = capsys.readouterr()
    assert "Bumped pyproject.toml" in captured.out
    assert "Bumped README.md" in captured.out
