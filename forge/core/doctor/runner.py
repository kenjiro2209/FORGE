from forge.core.doctor.python import check as check_python
from forge.core.doctor.git import check as check_git
from forge.core.doctor.freecad import check as check_freecad


def run():
    return [
        check_python(),
        check_git(),
        check_freecad(),
    ]