from __future__ import annotations

import tomllib
import typing as t
from pathlib import Path

from packaging import version

BUMPER_REQUIRED_FIELDS = ("current_version",)
REPLACEMENT_REQUIRED_FIELDS = ("file", "search")


class BumperConfigError(Exception): ...  # noqa: D101


class BumperFile(t.NamedTuple):  # noqa: D101
    file: Path
    search: str

    @classmethod
    def from_toml(cls, file: str, search: str) -> BumperFile:  # noqa: D102
        return cls(file=Path(file), search=search)


def _validate_config(cfg: dict) -> None:
    """
    Validate the provided parsed TOML output.

    The provided TOML is assumed to contain something like the following:

    ```toml
    [tool.bumper]
    current_version = "0.1.0"

    [[tool.bumper.files]]
    file = "./pyproject.toml"
    search = 'version = "{current_version}"'
    ```

    Raises `BumperConfigError` if any of the required information is missing.
    """
    if "tool" not in cfg:
        raise BumperConfigError("Configuration file does not declare any tools")

    if "bumper" not in cfg["tool"]:
        raise BumperConfigError("Configuration does not declare any bumper configuration")

    for rf in BUMPER_REQUIRED_FIELDS:
        if rf not in cfg["tool"]["bumper"]:
            raise BumperConfigError(f"Bumper tool declaration missing required field: '{rf}'")

    if "files" not in cfg["tool"]["bumper"]:
        raise BumperConfigError("Configuration does not declare any file replacements")

    for file in cfg["tool"]["bumper"]["files"]:
        for rf in REPLACEMENT_REQUIRED_FIELDS:
            if rf not in file:
                raise BumperConfigError(
                    f"File replacement declaration missing required field: '{rf}'"
                )


PARSED_T: t.TypeAlias = tuple[version.Version, list[BumperFile]]


def parse_config(cfg_path: Path) -> PARSED_T:
    """
    Parse the provided configuration file for its relevant information.

    Incoming information relevant to bumper is validated & extracted for downstream use.
    """
    if not cfg_path.exists():
        raise ValueError(f"Configuration file does not exist: '{cfg_path}'")

    with cfg_path.open("rb") as f:
        loaded = tomllib.load(f)

    _validate_config(loaded)
    current_version = version.parse(loaded["tool"]["bumper"]["current_version"])
    files = [BumperFile.from_toml(**f) for f in loaded["tool"]["bumper"]["files"]]

    return current_version, files
