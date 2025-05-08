from pathlib import Path

import pytest

from bumper.config import ExistingConfigError, VersioningType, write_default_config

STARTER_CONFIG_SEMVER = """\
[tool.bumper]
current_version = "0.1.0"
versioning_type = "semver"

[[tool.bumper.files]]
file = "./pyproject.toml"
search = 'version = "{current_version}"'
"""


def test_write_default_config_no_existing(tmp_path: Path) -> None:
    write_default_config(root_dir=tmp_path)

    cfg_path = tmp_path / ".bumper.toml"
    assert cfg_path.read_text() == STARTER_CONFIG_SEMVER


def test_write_default_config_existing_config_ignore_overwrites(tmp_path: Path) -> None:
    cfg_path = tmp_path / ".bumper.toml"
    cfg_path.touch()

    write_default_config(ignore_existing=True, root_dir=tmp_path)
    assert cfg_path.read_text() == STARTER_CONFIG_SEMVER


def test_write_default_config_existing_config_no_ignore_raises(tmp_path: Path) -> None:
    (tmp_path / ".bumper.toml").touch()
    with pytest.raises(ExistingConfigError, match="exists"):
        write_default_config(ignore_existing=False, root_dir=tmp_path)


STARTER_CONFIG_CALVER = """\
[tool.bumper]
current_version = "2025.01.0"
versioning_type = "calver"

[[tool.bumper.files]]
file = "./pyproject.toml"
search = 'version = "{current_version}"'
"""


def test_write_default_config_calver(tmp_path: Path) -> None:
    write_default_config(versioning_type=VersioningType.CALVER, root_dir=tmp_path)

    cfg_path = tmp_path / ".bumper.toml"
    assert cfg_path.read_text() == STARTER_CONFIG_CALVER
