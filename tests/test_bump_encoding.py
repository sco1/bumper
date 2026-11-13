import io
from pathlib import Path

import pytest
from packaging.version import Version

from bumper.bump import BumpType, bump_ver
from bumper.config import BumperFile

# "Á" encodes to b"\xc3\x81" in UTF-8; 0x81 is undefined in cp1252 so a cp1252 read raises
# UnicodeDecodeError. "🐍" can't be encoded to cp1252 so a cp1252 write raises UnicodeEncodeError.
NON_ASCII_SRC = '[project]\nversion = "0.1.0"\nauthors = ["Ágnes Café 🐍"]\n'.encode("utf-8")


@pytest.fixture
def cp1252_locale(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Simulate a non-UTF-8 locale encoding, e.g. Windows w/Python < 3.15.

    `pathlib`'s text I/O methods resolve an unspecified `encoding` via `io.text_encoding`, so
    patching it allows us to simulate the locale-dependent default regardless of the host platform.

    NOTE: The builtin `open()` does not call `io.text_encoding`, so this does not catch a regression
    introduced by a builtin `open()` call that omits `encoding`.
    """

    def _cp1252_default(encoding: str | None, stacklevel: int = 2) -> str:
        return "cp1252" if encoding is None else encoding

    monkeypatch.setattr(io, "text_encoding", _cp1252_default)


@pytest.mark.usefixtures("cp1252_locale")
def test_bump_non_ascii_file_round_trip(tmp_path: Path) -> None:
    target = tmp_path / "pyproject.toml"
    target.write_bytes(NON_ASCII_SRC)

    bump_ver(
        current_version=Version("0.1.0"),
        files=[BumperFile(file=target, search='version = "{current_version}"')],
        bump_type=BumpType.PATCH,
        dry_run=False,
    )

    truth_out = NON_ASCII_SRC.replace(b'version = "0.1.0"', b'version = "0.1.1"')
    assert target.read_bytes() == truth_out


@pytest.mark.usefixtures("cp1252_locale")
def test_bump_non_ascii_search(tmp_path: Path) -> None:
    target = tmp_path / "README.md"
    target.write_bytes("Café release: v0.1.0\n".encode("utf-8"))

    bump_ver(
        current_version=Version("0.1.0"),
        files=[BumperFile(file=target, search="Café release: v{current_version}")],
        bump_type=BumpType.PATCH,
        dry_run=False,
    )

    assert target.read_bytes() == "Café release: v0.1.1\n".encode("utf-8")


@pytest.mark.usefixtures("cp1252_locale")
def test_patched_locale_sanity(tmp_path: Path) -> None:
    # Guard against the fixture silently becoming a no-op, e.g. if pathlib stops routing through
    # io.text_encoding in a future Python version
    target = tmp_path / "sanity.txt"
    target.write_bytes(NON_ASCII_SRC)

    with pytest.raises(UnicodeDecodeError):
        target.read_text()
