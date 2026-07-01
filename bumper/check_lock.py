import tomllib
import typing as t
from pathlib import Path


class ProjectMetadata(t.NamedTuple):
    name: str
    ver: str


def _get_project_info(pyproject: Path) -> ProjectMetadata:
    with pyproject.open("rb") as f:
        pyproject_data = tomllib.load(f)

    metadata = pyproject_data.get("project")
    if metadata is None:
        raise ValueError("`project` table could not be located.")

    project_name = metadata.get("name")
    project_ver = metadata.get("version")

    if not project_name:
        raise ValueError("'project' table has no 'name' key.")
    if not project_ver:
        raise ValueError("'project' table has no 'version' key.")

    return ProjectMetadata(name=project_name, ver=project_ver)


def _get_project_lock_info(lockfile: Path, project_name: str) -> str:
    with lockfile.open("rb") as f:
        lockfile_data = tomllib.load(f)

    for p in lockfile_data["package"]:
        # I'm not sure if there's a possibility for our own project to be mentioned twice, for now
        # assume not
        if p["name"] == project_name:
            return p["version"]  # type: ignore[no-any-return]
    else:
        raise ValueError(f"Could not locate project '{project_name}' in lockfile.")


def is_local_locked(
    pyproject: Path = Path("./pyproject.toml"), lockfile: Path = Path("./uv.lock")
) -> bool:
    """Check that the local project version is matched between `pyproject.toml` and `uv.lock`."""
    if not lockfile.exists():
        raise ValueError(f"Lockfile does not exist at: {lockfile}")
    if not pyproject.exists():
        raise ValueError(f"pyproject.toml does not exist at: {pyproject}")

    project_metadata = _get_project_info(pyproject)
    locked_ver = _get_project_lock_info(lockfile, project_metadata.name)

    return project_metadata.ver == locked_ver
