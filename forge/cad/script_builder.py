from pathlib import Path

CAD_FORMATS = {".step", ".stp", ".iges", ".igs"}
MESH_FORMATS = {".stl", ".obj"}
DXF_FORMATS = {".dxf"}
SVG_FORMATS = {".svg"}


class ScriptBuilder:

    def __init__(self):
        self.lines = []
        self._counter = 0
        self.objects: list[str] = []

    def add(self, line: str):
        self.lines.append(line)

    def next_var(self, prefix: str = "v") -> str:
        """Genera un nombre de variable unico para el script generado."""
        self._counter += 1
        return f"{prefix}_{self._counter}"

    def register_object(self, var_name: str):
        """Registra un objeto de FreeCAD (doc.addObject(...)) para exportarlo luego."""
        self.objects.append(var_name)

    def begin_document(self, name: str):
        self.add("import FreeCAD")
        self.add("import Part")
        self.add("import Import")
        self.add("import Mesh")
        self.add("")
        self.add(f'doc = FreeCAD.newDocument("{name}")')
        self.add("")

    def end_document(self):
        self.add("")
        self.add("doc.recompute()")

    def save_fcstd(self, path: str):
        self.add("")
        self.add(f'doc.saveAs(r"{path}")')

    def export(self, path: str):
        """Exporta los objetos registrados al formato indicado por la extension del path.

        Soporta:
        - STEP / IGES (solidos, via Import.export)
        - STL / OBJ (mallas, via Mesh.export)
        - DXF / SVG (proyeccion 2D del solido, via importDXF/importSVG)
        """

        if not self.objects:
            raise ValueError(
                "No hay objetos registrados para exportar. "
                "Cada operacion debe llamar builder.register_object(...)."
            )

        extension = Path(path).suffix.lower()
        objects_list = ", ".join(self.objects)

        self.add("")

        if extension in CAD_FORMATS:
            self.add(f'Import.export([{objects_list}], r"{path}")')
        elif extension in MESH_FORMATS:
            self.add(f'Mesh.export([{objects_list}], r"{path}")')
        elif extension in DXF_FORMATS:
            self.add("import importDXF")
            self.add(f'importDXF.export([{objects_list}], r"{path}")')
        elif extension in SVG_FORMATS:
            self.add("import importSVG")
            self.add(f'importSVG.export([{objects_list}], r"{path}")')
        else:
            raise ValueError(f"Formato de exportacion no soportado: '{extension}'")

    def export_step(self, path: str):
        """Alias retrocompatible de export() para STEP."""
        self.export(path)

    def write(self, path: Path):
        path.write_text("\n".join(self.lines), encoding="utf-8")