import typing as t

import typer

from bumper import CONFIG_PRIORITY
from bumper.bump import BumpType, bump_ver
from bumper.config import (
    BumperConfigError,
    BumperFile,
    ExistingConfigError,
    VersioningType,
    parse_config,
    write_default_config,
)

bumper_cli = typer.Typer(add_completion=False)


def _abort_with_message(message: str, end: str = "\n") -> t.Never:
    print(message, end=end)
    raise typer.Abort()


@bumper_cli.command(name="bump")
def bump_ver_cmd(
    bump_by: BumpType,
    dry_run: bool = typer.Option(False, help="Preview the requested diff."),
) -> None:
    """
    Bump the requested version component.

    Allowable `BUMP_BY` values differ based on the project's specified versioning type: SemVer -
    (major, minor, patch), CalVer - (date)

    When using CalVer, if the user's current UTC month is the same as the current project version,
    then the Micro component is incremented. Otherwise, the date components are bumped to the user's
    current UTC month and Micro reset to `0`.

    If `dry_run` is `True`, the requested diff will be displayed in the terminal & no file
    modifications will take place.
    """
    for cfg_path in CONFIG_PRIORITY:
        if cfg_path.exists():
            break
    else:
        _abort_with_message("Configuration file could not be located.")

    try:
        current_version, versioning_type, files = parse_config(cfg_path)
    except BumperConfigError as e:
        _abort_with_message(str(e))

    # Check valid bump_by before we attempt to build a new version
    if versioning_type == VersioningType.SEMVER:
        if bump_by == BumpType.DATE:
            _abort_with_message("SemVer projects must bump by major, minor, or patch.")
    elif versioning_type == VersioningType.CALVER:
        if bump_by != BumpType.DATE:
            _abort_with_message("CalVer projects must bump by date.")

    # Add in the bump configuration so it gets updated as well
    files.append(BumperFile(file=cfg_path, search='current_version = "{current_version}"'))
    bump_ver(current_version=current_version, files=files, bump_type=bump_by, dry_run=dry_run)


@bumper_cli.command()
def init(
    versioning_type: VersioningType = VersioningType.SEMVER,
    ignore_existing: bool = typer.Option(False),
) -> None:
    """
    Generate a default bumper configuration file.

    If the `--ignore_existing` flag is set, any existing `.bumper.toml` file will be overwritten;
    this action is not reversible. Otherwise, the existing configuration will be preserved.
    """
    try:
        write_default_config(versioning_type=versioning_type, ignore_existing=ignore_existing)
    except ExistingConfigError as e:
        _abort_with_message(str(e))


if __name__ == "__main__":
    bumper_cli()
