from forge.cad.components.rectangle import Rectangle
from forge.cad.model import Model
from forge.cad.operations.extrude import Extrude
from forge.cad.operations.union import Union
from forge.cad.sketch.face import Face
from forge.cad.sketch.wire import Wire


def make_extrude(width, height, depth):
    sketch = Rectangle(width=width, height=height).build()
    wire = Wire.from_sketch(sketch)
    face = Face(wire)
    return Extrude(face=face, height=depth)


def test_union_registers_single_object():
    box_a = make_extrude(40, 20, 10)
    box_b = make_extrude(20, 40, 10)
    union = Union(base=box_a, tool=box_b)

    model = Model("union_test")
    model.add(union)

    assert model.operations == [union]