import subprocess

from forge.core.doctor.base import CheckResult


def check() -> CheckResult:
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )

        version = result.stdout.strip().replace("git version ", "")

        return CheckResult(
            name="Git",
            success=True,
            version=version,
        )

    except (subprocess.CalledProcessError, FileNotFoundError):
        return CheckResult(
            name="Git",
            success=False,
            message="Git is not installed.",
        )