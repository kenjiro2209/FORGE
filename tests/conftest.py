from __future__ import annotations

import pytest


class FakeBuilder:
    """Doble de prueba de ScriptBuilder: no genera FreeCAD real,
    solo registra las líneas y variables como lo haría el builder real.
    Permite testear la lógica de las operaciones sin depender de FreeCAD.
    """

    def __init__(self):
        self.lines: list[str] = []
        self.objects: list[str] = []
        self._counter = 0

    def add(self, line: str):
        self.lines.append(line)

    def next_var(self, prefix: str = "v") -> str:
        self._counter += 1
        return f"{prefix}_{self._counter}"

    def register_object(self, var_name: str):
        self.objects.append(var_name)


@pytest.fixture
def builder():
    return FakeBuilder()