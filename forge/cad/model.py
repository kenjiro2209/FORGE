from pathlib import Path

from forge.cad.script_builder import ScriptBuilder

DEFAULT_FORMATS: tuple[str, ...] = ("step",)


class Model:

    def __init__(self, name: str):
        self.name = name
        self.operations = []

    def add(self, operation):
        self.operations.append(operation)
        return operation

    def build(
        self,
        script_path: Path,
        output_path: Path,
        formats: tuple[str, ...] = DEFAULT_FORMATS,
    ):
        builder = ScriptBuilder()
        builder.begin_document(self.name)

        for operation in self.operations:
            operation.build(builder)
            builder.register_object(operation.obj_var)

        builder.end_document()
        builder.save_fcstd(str(output_path / f"{self.name}.FCStd"))

        for fmt in formats:
            builder.export(str(output_path / f"{self.name}.{fmt}"))

        builder.write(script_path)