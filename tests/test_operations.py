from __future__ import annotations

import pytest

from forge.cad.components.rectangle import Rectangle
from forge.cad.operations.chamfer import Chamfer
from forge.cad.operations.cut import Cut
from forge.cad.operations.extrude import Extrude
from forge.cad.operations.fillet import Fillet
from forge.cad.operations.intersection import Intersection
from forge.cad.operations.transform import Transform
from forge.cad.operations.union import Union
from forge.cad.geometry.vector import Vector
from forge.cad.sketch.face import Face
from forge.cad.sketch.wire import Wire


def make_extrude(width=40, height=20, depth=10):
    sketch = Rectangle(width=width, height=height).build()
    wire = Wire.from_sketch(sketch)
    face = Face(wire)
    return Extrude(face=face, height=depth)


def test_extrude_rejects_zero_or_negative_height():
    sketch = Rectangle(width=10, height=10).build()
    face = Face(Wire.from_sketch(sketch))
    with pytest.raises(ValueError):
        Extrude(face=face, height=0)


def test_extrude_builds_and_sets_obj_var(builder):
    extrude = make_extrude()
    obj_var = extrude.build(builder)

    assert obj_var == extrude.obj_var
    assert any("extrude" in line for line in builder.lines)


def test_union_builds_nested_operations_once(builder):
    box_a = make_extrude(40, 20, 10)
    box_b = make_extrude(20, 40, 10)
    union = Union(base=box_a, tool=box_b)

    union.build(builder)

    assert box_a.obj_var is not None
    assert box_b.obj_var is not None
    assert any(".fuse(" in line for line in builder.lines)


def test_cut_builds_nested_operations_once(builder):
    box_a = make_extrude(40, 20, 10)
    box_b = make_extrude(20, 40, 10)
    cut = Cut(base=box_a, tool=box_b)

    cut.build(builder)

    assert any(".cut(" in line for line in builder.lines)


def test_intersection_builds_common(builder):
    box_a = make_extrude(40, 20, 10)
    box_b = make_extrude(20, 40, 10)
    intersection = Intersection(base=box_a, tool=box_b)

    intersection.build(builder)

    assert any(".common(" in line for line in builder.lines)


def test_transform_applies_translation(builder):
    box = make_extrude()
    transform = Transform(box, translation=Vector(5, 0, 0))

    transform.build(builder)

    assert any("FreeCAD.Placement" in line for line in builder.lines)


def test_fillet_rejects_zero_or_negative_radius():
    box = make_extrude()
    with pytest.raises(ValueError):
        Fillet(box, radius=0)


def test_fillet_applies_to_all_edges_by_default(builder):
    box = make_extrude()
    fillet = Fillet(box, radius=2)

    fillet.build(builder)

    assert any("makeFillet" in line and ".Edges" in line for line in builder.lines)


def test_fillet_applies_to_specific_edges(builder):
    box = make_extrude()
    fillet = Fillet(box, radius=2, edges=[0, 2])

    fillet.build(builder)

    assert any("for i in (0, 2,)" in line for line in builder.lines)


def test_chamfer_rejects_zero_or_negative_distance():
    box = make_extrude()
    with pytest.raises(ValueError):
        Chamfer(box, distance=0)


def test_chamfer_applies_to_all_edges_by_default(builder):
    box = make_extrude()
    chamfer = Chamfer(box, distance=1)

    chamfer.build(builder)

    assert any("makeChamfer" in line and ".Edges" in line for line in builder.lines)