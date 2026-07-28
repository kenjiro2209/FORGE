from pathlib import Path

from forge.cad.freecad_runner import run_script
from forge.cad.model import DEFAULT_FORMATS, Model


OUTPUT_DIR = Path("forge/output")
SCRIPT_DIR = Path("forge/cad/scripts")


def build(model: Model, formats: tuple[str, ...] = DEFAULT_FORMATS):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    script_path = SCRIPT_DIR / f"{model.name.lower()}.py"

    model.build(
        script_path=script_path,
        output_path=OUTPUT_DIR,
        formats=formats,
    )

    result = run_script(script_path)

    return result