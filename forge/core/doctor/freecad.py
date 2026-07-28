import subprocess

from forge.cad.freecad_loader import find_freecad_cmd
from forge.core.doctor.base import CheckResult


def check() -> CheckResult:
    freecad_cmd = find_freecad_cmd()

    if freecad_cmd is None:
        return CheckResult(name="FreeCAD", success=False, message="FreeCAD no fue encontrado en el sistema.")

    try:
        result = subprocess.run([str(freecad_cmd), "--version"], capture_output=True, text=True, check=True)
        return CheckResult(name="FreeCAD", success=True, version=result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return CheckResult(name="FreeCAD", success=False, message=f"Se encontro FreeCAD en {freecad_cmd} pero no se pudo ejecutar.")