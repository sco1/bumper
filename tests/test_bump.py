from pathlib import Path

import pytest
from packaging.version import Version

from bumper.bump import BumpType, _build_new_version, _merge_bumpers, bump_ver
from bumper.config import BumperFile

VERSION_BUILD_TEST_CASES = (
    (Version("0.0.1"), BumpType.MAJOR, Version("1.0.0")),
    (Version("0.0.1"), BumpType.MINOR, Version("0.1.0")),
    (Version("0.0.1"), BumpType.PATCH, Version("0.0.2")),
    (Version("0.1.0"), BumpType.MAJOR, Version("1.0.0")),
    (Version("0.1.0"), BumpType.MINOR, Version("0.2.0")),
    (Version("0.1.0"), BumpType.PATCH, Version("0.1.1")),
    (Version("1.0.0"), BumpType.MAJOR, Version("2.0.0")),
    (Version("1.0.0"), BumpType.MINOR, Version("1.1.0")),
    (Version("1.0.0"), BumpType.PATCH, Version("1.0.1")),
    (Version("1.0"), BumpType.MAJOR, Version("2.0.0")),
    (Version("1.0"), BumpType.MINOR, Version("1.1.0")),
    (Version("1.0"), BumpType.PATCH, Version("1.0.1")),
)


@pytest.mark.parametrize(("current_version", "bump_type", "truth_out"), VERSION_BUILD_TEST_CASES)
def test_version_build(current_version: Version, bump_type: BumpType, truth_out: Version) -> None:
    assert _build_new_version(current_version, bump_type) == truth_out


def test_merge_bumpers() -> None:
    files = [
        BumperFile(file=Path("./pyproject.toml"), search='version = "{current_version}"'),
        BumperFile(file=Path("./README.md"), search="sco1-bumper/{current_version}"),
        BumperFile(file=Path("./README.md"), search="rev: v{current_version}"),
    ]

    truth_out = {
        Path("./pyproject.toml"): ['version = "{current_version}"'],
        Path("./README.md"): ["sco1-bumper/{current_version}", "rev: v{current_version}"],
    }

    assert _merge_bumpers(files) == truth_out


SAMPLE_README = """\
# bumper
[![PyPI - Python Version](https://some.url/sco1-bumper/0.1.0?logo=python)]

Automatically increment the project's version number.

```yaml
repos:
-   repo: https://github.com/sco1/brie-commit
    rev: v0.1.0
    hooks:
    -   id: brie-commit
```
"""

TRUTH_BUMPED_README = """\
# bumper
[![PyPI - Python Version](https://some.url/sco1-bumper/0.2.0?logo=python)]

Automatically increment the project's version number.

```yaml
repos:
-   repo: https://github.com/sco1/brie-commit
    rev: v0.2.0
    hooks:
    -   id: brie-commit
```
"""

SAMPLE_PYPROJECT = """\
[project]
name = "sco1-bumper"
version = "0.1.0"
description = "Automatically increment the project's version number."

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

TRUTH_BUMPED_PYPROJECT = """\
[project]
name = "sco1-bumper"
version = "0.2.0"
description = "Automatically increment the project's version number."

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""


@pytest.fixture
def dummy_repo(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text(SAMPLE_README)
    (tmp_path / "pyproject.toml").write_text(SAMPLE_PYPROJECT)

    return tmp_path


def test_bump_ver_single_replace(dummy_repo: Path) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
    ]

    bump_ver(current_version=Version("0.1.0"), files=files, bump_type=BumpType.MINOR, dry_run=False)

    assert pyproject.read_text() == TRUTH_BUMPED_PYPROJECT


TRUTH_SINGLE_DIFF = """\
--- pyproject.toml
+++
@@ -3 +3 @@
-version = "0.1.0"
+version = "0.2.0"
"""


def test_bump_ver_single_replace_dry_run(dummy_repo: Path, capsys: pytest.CaptureFixture) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
    ]

    bump_ver(current_version=Version("0.1.0"), files=files, bump_type=BumpType.MINOR, dry_run=True)

    assert pyproject.read_text() == SAMPLE_PYPROJECT

    captured = capsys.readouterr()
    assert captured.out == TRUTH_SINGLE_DIFF


def test_bump_ver_multi_replace(dummy_repo: Path) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    readme = dummy_repo / "README.md"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
        BumperFile(file=readme, search="sco1-bumper/{current_version}"),
        BumperFile(file=readme, search="rev: v{current_version}"),
    ]

    bump_ver(current_version=Version("0.1.0"), files=files, bump_type=BumpType.MINOR, dry_run=False)

    assert pyproject.read_text() == TRUTH_BUMPED_PYPROJECT
    assert readme.read_text() == TRUTH_BUMPED_README


TRUTH_MULTI_DIFF = """\
--- pyproject.toml
+++
@@ -3 +3 @@
-version = "0.1.0"
+version = "0.2.0"
--- README.md
+++
@@ -2 +2 @@
-[![PyPI - Python Version](https://some.url/sco1-bumper/0.1.0?logo=python)]
+[![PyPI - Python Version](https://some.url/sco1-bumper/0.2.0?logo=python)]
@@ -9 +9 @@
-    rev: v0.1.0
+    rev: v0.2.0
"""


def test_bump_ver_multi_replace_dry_run(dummy_repo: Path, capsys: pytest.CaptureFixture) -> None:
    pyproject = dummy_repo / "pyproject.toml"
    readme = dummy_repo / "README.md"
    files = [
        BumperFile(file=pyproject, search='version = "{current_version}"'),
        BumperFile(file=readme, search="sco1-bumper/{current_version}"),
        BumperFile(file=readme, search="rev: v{current_version}"),
    ]

    bump_ver(current_version=Version("0.1.0"), files=files, bump_type=BumpType.MINOR, dry_run=True)

    assert pyproject.read_text() == SAMPLE_PYPROJECT
    assert readme.read_text() == SAMPLE_README

    captured = capsys.readouterr()
    assert captured.out == TRUTH_MULTI_DIFF
