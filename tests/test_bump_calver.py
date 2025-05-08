import datetime as dt

import pytest
import time_machine
from packaging.version import Version

from bumper.bump import BumpType, _build_new_version

CALVER_TEST_CASES = (
    (Version("2025.01.0"), dt.date(year=2025, month=1, day=1), Version("2025.01.1")),
    (Version("2025.01"), dt.date(year=2025, month=1, day=1), Version("2025.01.1")),
    (Version("2025.10.0"), dt.date(year=2025, month=10, day=1), Version("2025.10.1")),
    (Version("2025.10"), dt.date(year=2025, month=10, day=1), Version("2025.10.1")),
    (Version("2025.01.0"), dt.date(year=2025, month=2, day=1), Version("2025.02.0")),
    (Version("2025.01.1"), dt.date(year=2025, month=2, day=1), Version("2025.02.0")),
    (Version("2025.10.0"), dt.date(year=2025, month=11, day=1), Version("2025.11.0")),
    (Version("2025.10.1"), dt.date(year=2025, month=11, day=1), Version("2025.11.0")),
)


@pytest.mark.parametrize(("current_version", "current_date", "truth_out"), CALVER_TEST_CASES)
def test_calver_version_build(
    current_version: Version,
    current_date: dt.date,
    truth_out: Version,
) -> None:
    with time_machine.travel(current_date, tick=False):
        new_ver = _build_new_version(current_version=current_version, bump_type=BumpType.DATE)

    assert new_ver == truth_out
