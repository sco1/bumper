import copy
import difflib
from collections import defaultdict
from enum import StrEnum
from pathlib import Path

from packaging import version

from bumper.config import BumperFile


class BumpType(StrEnum):  # noqa: D101
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


def _build_new_version(current_version: version.Version, bump_type: BumpType) -> version.Version:
    major, minor, patch = current_version.major, current_version.minor, current_version.micro
    if bump_type is BumpType.MAJOR:
        new_version = version.Version(f"{major+1}.0.0")
    elif bump_type is BumpType.MINOR:
        new_version = version.Version(f"{major}.{minor+1}.0")
    elif bump_type is BumpType.PATCH:  # pragma: no branch
        new_version = version.Version(f"{major}.{minor}.{patch+1}")

    return new_version


def _merge_bumpers(files: list[BumperFile]) -> dict[Path, list[str]]:
    """Consolidate bump specifications per-file for downstream use."""
    file_operations = defaultdict(list)
    for b in files:
        file_operations[b.file].append(b.search)

    return file_operations


def bump_ver(
    current_version: version.Version, files: list[BumperFile], bump_type: BumpType, dry_run: bool
) -> None:
    """
    Bump the current version according to the provided rules in `files`.

    **NOTE:** Ensure that the bumper configuration file is included in the rules passed to `files`.

    If `dry_run` is `True`, files will not be modified and a per-file diff will be printed to the
    terminal instead.
    """
    next_version = _build_new_version(current_version, bump_type)
    file_operations = _merge_bumpers(files)  # Merge so we handle each file all at once

    for target_file, rules in file_operations.items():
        old = target_file.read_text()
        new = copy.copy(old)

        for r in rules:
            new = new.replace(
                r.replace("{current_version}", str(current_version)),
                r.replace("{current_version}", str(next_version)),
            )

        if dry_run:
            diff = difflib.unified_diff(
                old.splitlines(), new.splitlines(), fromfile=target_file.name, n=0, lineterm=""
            )
            # Strip trailing whitespace to make testing easier
            print("\n".join(line.rstrip() for line in diff))
        else:
            target_file.write_text(new)
