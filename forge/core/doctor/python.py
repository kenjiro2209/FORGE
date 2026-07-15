import sys

from forge.core.doctor.base import CheckResult


def check() -> CheckResult:
    return CheckResult(
        name="Python",
        success=sys.version_info >= (3, 13),
        version=sys.version.split()[0],
    )