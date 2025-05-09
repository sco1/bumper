from pathlib import Path

import pytest

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

SAMPLE_PYPROJECT = """\
[project]
name = "sco1-bumper"
version = "0.1.0"
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
