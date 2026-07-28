from __future__ import annotations

import platform
import shutil
from pathlib import Path


def find_freecad_cmd() -> Path | None:
    """Busca el ejecutable FreeCADCmd en el sistema, sin depender del OS."""

    from_path = shutil.which("FreeCADCmd") or shutil.which("freecadcmd")
    if from_path:
        return Path(from_path)

    system = platform.system()
    candidates: list[Path] = []

    if system == "Windows":
        program_dirs = [Path(r"C:\Program Files"), Path(r"C:\Program Files (x86)")]
        for program_dir in program_dirs:
            if program_dir.exists():
                candidates.extend(program_dir.glob("FreeCAD*/bin/FreeCADCmd.exe"))

    elif system == "Darwin":
        candidates.append(Path("/Applications/FreeCAD.app/Contents/Resources/bin/FreeCADCmd"))

    elif system == "Linux":
        candidates.extend([
            Path("/usr/bin/FreeCADCmd"),
            Path("/usr/local/bin/FreeCADCmd"),
            Path("/snap/bin/freecad.FreeCADCmd"),
        ])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None