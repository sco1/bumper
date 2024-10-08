from pathlib import Path

import pytest

from bumper.config import ExistingConfigError, STARTER_CONFIG, write_default_config


def test_write_default_config_no_existing(tmp_path: Path) -> None:
    write_default_config(root_dir=tmp_path)

    cfg_path = tmp_path / ".bumper.toml"
    assert cfg_path.read_text() == STARTER_CONFIG


def test_write_default_config_existing_config_ignore_overwrites(tmp_path: Path) -> None:
    cfg_path = tmp_path / ".bumper.toml"
    cfg_path.touch()

    write_default_config(ignore_existing=True, root_dir=tmp_path)
    assert cfg_path.read_text() == STARTER_CONFIG


def test_write_default_config_existing_config_no_ignore_raises(tmp_path: Path) -> None:
    (tmp_path / ".bumper.toml").touch()
    with pytest.raises(ExistingConfigError, match="exists"):
        write_default_config(ignore_existing=False, root_dir=tmp_path)
