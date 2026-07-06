from pathlib import Path

import pytest

from bumper.check_lock import (
    ProjectMetadata,
    _get_project_info,
    _get_project_lock_info,
    is_local_locked,
)

SAMPLE_PYPROJECT_NO_PROJECT = """\
readme = "README.md"
classifiers = [
    "Programming Language :: Python :: 3.14",
]
"""


def test_pyproject_no_project_table_raises(tmp_path: Path) -> None:
    pp = tmp_path / "pyproject.toml"
    pp.write_text(SAMPLE_PYPROJECT_NO_PROJECT)

    with pytest.raises(ValueError, match="'project' table"):
        _get_project_info(pp)


SAMPLE_PYPROJECT_NO_NAME = """\
[project]
version = "2.0.3"
description = "Automatically increment the project's version number."
license = "MIT"
"""


def test_pyproject_no_project_name_raises(tmp_path: Path) -> None:
    pp = tmp_path / "pyproject.toml"
    pp.write_text(SAMPLE_PYPROJECT_NO_NAME)

    with pytest.raises(ValueError, match="'name' key"):
        _get_project_info(pp)


SAMPLE_PYPROJECT_NO_VER = """\
[project]
name = "sco1-bumper"
description = "Automatically increment the project's version number."
license = "MIT"
"""


def test_pyproject_no_project_ver_raises(tmp_path: Path) -> None:
    pp = tmp_path / "pyproject.toml"
    pp.write_text(SAMPLE_PYPROJECT_NO_VER)

    with pytest.raises(ValueError, match="'version' key"):
        _get_project_info(pp)


SAMPLE_PYPROJECT = """\
[project]
name = "sco1-bumper"
version = "2.0.3"
description = "Automatically increment the project's version number."
license = "MIT"
"""

TRUTH_PYPROJECT_META = ProjectMetadata(name="sco1-bumper", ver="2.0.3")


def test_get_project_info(tmp_path: Path) -> None:
    pp = tmp_path / "pyproject.toml"
    pp.write_text(SAMPLE_PYPROJECT)

    assert _get_project_info(pp) == TRUTH_PYPROJECT_META


SAMPLE_LOCK_NO_LOCAL = """\
[[package]]
name = "flake8-annotations"
version = "3.2.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "flake8" },
]
sdist = { url = "abc", hash = "123", size = 14169, upload-time = "2025-10-09T21:17:57.816Z" }
wheels = [
    { url = "abc", hash = "123", size = 16873, upload-time = "2025-10-09T21:17:56.265Z" },
]
"""


def test_get_project_lock_info_no_local_raises(tmp_path: Path) -> None:
    lf = tmp_path / "uv.lock"
    lf.write_text(SAMPLE_LOCK_NO_LOCAL)

    with pytest.raises(ValueError, match="Could not locate project"):
        _get_project_lock_info(lf, "sco1-bumper")


SAMPLE_LOCK = """\
[[package]]
name = "flake8-annotations"
version = "3.2.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "flake8" },
]
sdist = { url = "abc", hash = "123", size = 14169, upload-time = "2025-10-09T21:17:57.816Z" }
wheels = [
    { url = "abc", hash = "123", size = 16873, upload-time = "2025-10-09T21:17:56.265Z" },
]

[[package]]
name = "sco1-bumper"
version = "2.0.3"
source = { editable = "." }
dependencies = [
    { name = "packaging" },
    { name = "typer" },
]
"""


def test_get_project_lock_info(tmp_path: Path) -> None:
    lf = tmp_path / "uv.lock"
    lf.write_text(SAMPLE_LOCK)

    assert _get_project_lock_info(lf, "sco1-bumper") == "2.0.3"


def test_is_local_locked_no_lockfile_raises(tmp_path: Path) -> None:
    lf = tmp_path / "uv.lock"
    pp = tmp_path / "pyproject.toml"
    pp.write_text(SAMPLE_PYPROJECT)

    with pytest.raises(ValueError, match="Lockfile does not exist"):
        is_local_locked(pyproject=pp, lockfile=lf)


def test_is_local_locked_no_pyproject_raises(tmp_path: Path) -> None:
    pp = tmp_path / "pyproject.toml"
    lf = tmp_path / "uv.lock"
    lf.write_text(SAMPLE_LOCK)

    with pytest.raises(ValueError, match="pyproject.toml does not exist"):
        is_local_locked(pyproject=pp, lockfile=lf)


def test_is_local_locked(tmp_path: Path) -> None:
    pp = tmp_path / "pyproject.toml"
    pp.write_text(SAMPLE_PYPROJECT)

    lf = tmp_path / "uv.lock"
    lf.write_text(SAMPLE_LOCK)

    assert is_local_locked()
