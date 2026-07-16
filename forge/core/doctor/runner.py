from forge.core.doctor.python import check as check_python
from forge.core.doctor.git import check as check_git


def run():
    return [
        check_python(),
        check_git(),
    ]