import tomllib
from pathlib import Path

import pytest
from packaging import version

from bumper.config import (
    BumperConfigError,
    BumperFile,
    PARSED_T,
    VersioningType,
    _validate_config,
    parse_config,
)
from tests import TEST_DATA_DIR

TOML_NO_TOOLS = """\
[project]
name = "sco1-bumper"
version = "0.1.0"
"""


def test_config_validation_no_tool_raises() -> None:
    cfg = tomllib.loads(TOML_NO_TOOLS)
    with pytest.raises(BumperConfigError, match="tools"):
        _validate_config(cfg)


TOML_NO_BUMPER = """\
[tool.black]
line-length = 100
"""


def test_config_validation_no_bumper_raises() -> None:
    cfg = tomllib.loads(TOML_NO_BUMPER)
    with pytest.raises(BumperConfigError, match="bumper configuration"):
        _validate_config(cfg)


TOML_MISSING_BUMPER_INFO = """\
[tool.bumper]
hello_world = "hi"
versioning_type = "semver"
"""


def test_config_validation_missing_bumper_info_raises() -> None:
    cfg = tomllib.loads(TOML_MISSING_BUMPER_INFO)
    with pytest.raises(BumperConfigError, match="current_version"):
        _validate_config(cfg)


TOML_MISSING_FILES = """\
[tool.bumper]
current_version = "0.1.0"
versioning_type = "semver"
"""


def test_config_validation_no_files_raises() -> None:
    cfg = tomllib.loads(TOML_MISSING_FILES)
    with pytest.raises(BumperConfigError, match="any file replacements"):
        _validate_config(cfg)


TOML_MISSING_FILE_INFO = """\
[tool.bumper]
current_version = "0.1.0"
versioning_type = "semver"

[[tool.bumper.files]]
file = "./pyproject.toml"
"""


def test_config_validation_missing_file_info_raises() -> None:
    cfg = tomllib.loads(TOML_MISSING_FILE_INFO)
    with pytest.raises(BumperConfigError, match="search"):
        _validate_config(cfg)


def test_nonexistent_config_raises() -> None:
    with pytest.raises(ValueError, match="does not exist"):
        parse_config(Path("ooga.booga"))


TRUTH_SINGLE_REPLACE_SEMVER = (
    version.Version("0.1.0"),
    VersioningType.SEMVER,
    [BumperFile(file=Path("./pyproject.toml"), search='version = "{current_version}"')],
)
TRUTH_SINGLE_REPLACE_CALVER = (
    version.Version("2025.01.0"),
    VersioningType.CALVER,
    [BumperFile(file=Path("./pyproject.toml"), search='version = "{current_version}"')],
)

TRUTH_MULTI_REPLACE_SEMVER = (
    version.Version("0.1.0"),
    VersioningType.SEMVER,
    [
        BumperFile(file=Path("./pyproject.toml"), search='version = "{current_version}"'),
        BumperFile(file=Path("./README.md"), search="sco1-bumper/{current_version}"),
        BumperFile(file=Path("./README.md"), search="rev: v{current_version}"),
    ],
)
TRUTH_MULTI_REPLACE_CALVER = (
    version.Version("2025.01.0"),
    VersioningType.CALVER,
    [
        BumperFile(file=Path("./pyproject.toml"), search='version = "{current_version}"'),
        BumperFile(file=Path("./README.md"), search="sco1-bumper/{current_version}"),
        BumperFile(file=Path("./README.md"), search="rev: v{current_version}"),
    ],
)

CONFIG_PARSER_TEST_CASES = (
    (TEST_DATA_DIR / "sample_config.toml", TRUTH_SINGLE_REPLACE_SEMVER),
    (TEST_DATA_DIR / "sample_pyproject.toml", TRUTH_SINGLE_REPLACE_SEMVER),
    (TEST_DATA_DIR / "sample_config_multi_replace.toml", TRUTH_MULTI_REPLACE_SEMVER),
    (TEST_DATA_DIR / "sample_pyproject_multi_replace.toml", TRUTH_MULTI_REPLACE_SEMVER),
    (TEST_DATA_DIR / "sample_config_calver.toml", TRUTH_SINGLE_REPLACE_CALVER),
    (TEST_DATA_DIR / "sample_pyproject_calver.toml", TRUTH_SINGLE_REPLACE_CALVER),
)


@pytest.mark.parametrize(("cfg_path", "truth_parsed"), CONFIG_PARSER_TEST_CASES)
def test_config_parse(cfg_path: Path, truth_parsed: PARSED_T) -> None:
    assert parse_config(cfg_path) == truth_parsed
