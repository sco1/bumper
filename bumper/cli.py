import typing as t

import typer

from bumper import CONFIG_PRIORITY
from bumper.bump import BumpType, bump_ver
from bumper.config import (
    BumperConfigError,
    BumperFile,
    ExistingConfigError,
    parse_config,
    write_default_config,
)

bumper_cli = typer.Typer(add_completion=False)


class ConfigNotFoundError(Exception): ...  # noqa: D101


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

    If `dry_run` is `True`, the requested diff will be displayed in the terminal & no file
    modifications will take place.
    """
    for cfg_path in CONFIG_PRIORITY:
        if cfg_path.exists():
            break
    else:
        raise ConfigNotFoundError("Configuration file could not be located.")

    try:
        current_version, files = parse_config(cfg_path)
    except BumperConfigError as e:
        _abort_with_message(str(e))

    # Add in the bump configuration so it gets updated as well
    files.append(BumperFile(file=cfg_path, search='current_version = "{current_version}"'))
    bump_ver(current_version=current_version, files=files, bump_type=bump_by, dry_run=dry_run)


@bumper_cli.command()
def init(ignore_existing: bool = typer.Option(False)) -> None:
    """Generate a default bumper configuration file."""
    try:
        write_default_config(ignore_existing)
    except ExistingConfigError as e:
        _abort_with_message(str(e))


if __name__ == "__main__":
    bumper_cli()
