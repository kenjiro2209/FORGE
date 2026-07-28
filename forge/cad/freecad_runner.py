from __future__ import annotations

import subprocess
from pathlib import Path

from forge.cad.freecad_loader import find_freecad_cmd


class FreeCADNotFoundError(RuntimeError):
    """Se lanza cuando no se encuentra ninguna instalación de FreeCAD."""


class FreeCADExecutionError(RuntimeError):
    """Se lanza cuando FreeCADCmd ejecuta el script pero termina con error."""

    def __init__(self, script: Path, returncode: int, stderr: str):
        self.script = script
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(
            f"FreeCADCmd falló al ejecutar '{script}' (código {returncode}):\n{stderr}"
        )


class FreeCADTimeoutError(RuntimeError):
    """Se lanza cuando FreeCADCmd tarda más de lo permitido en ejecutar el script."""


def run_script(script: Path, timeout: float = 120.0) -> subprocess.CompletedProcess:
    """Ejecuta un script generado por ScriptBuilder usando FreeCADCmd.

    Lanza excepciones específicas en lugar de devolver un resultado
    crudo que el llamador tenga que interpretar manualmente.
    """

    freecad_cmd = find_freecad_cmd()

    if freecad_cmd is None:
        raise FreeCADNotFoundError(
            "No se encontró una instalación de FreeCAD. "
            "Instálalo o agrega FreeCADCmd al PATH del sistema."
        )

    if not script.exists():
        raise FileNotFoundError(f"El script '{script}' no existe.")

    try:
        result = subprocess.run(
            [str(freecad_cmd), str(script)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise FreeCADTimeoutError(
            f"FreeCADCmd no respondió en {timeout}s al ejecutar '{script}'."
        ) from exc

    if result.returncode != 0:
        raise FreeCADExecutionError(script, result.returncode, result.stderr)

    return result