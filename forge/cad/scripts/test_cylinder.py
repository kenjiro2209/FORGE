import FreeCAD
import Part
import Import

doc = FreeCAD.newDocument("test_cylinder")

p_1 = FreeCAD.Vector(0, 0, 0.0)
edge_2 = Part.makeCircle(15.0, p_1)
wire_3 = Part.Wire([edge_2])
face_4 = Part.Face(wire_3)
shape_5 = face_4.extrude(FreeCAD.Vector(0, 0, 20.0))
obj_6 = doc.addObject("Part::Feature", "Extrude")
obj_6.Shape = shape_5

doc.recompute()

doc.saveAs(r"forge\output\test_cylinder.FCStd")

Import.export([obj_6], r"forge\output\test_cylinder.step")