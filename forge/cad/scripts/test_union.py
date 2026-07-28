import FreeCAD
import Part
import Import

doc = FreeCAD.newDocument("test_union")

p_1 = FreeCAD.Vector(0, 0, 0.0)
p_2 = FreeCAD.Vector(40.0, 0, 0.0)
edge_3 = Part.makeLine(p_1, p_2)
p_4 = FreeCAD.Vector(40.0, 0, 0.0)
p_5 = FreeCAD.Vector(40.0, 20.0, 0.0)
edge_6 = Part.makeLine(p_4, p_5)
p_7 = FreeCAD.Vector(40.0, 20.0, 0.0)
p_8 = FreeCAD.Vector(0, 20.0, 0.0)
edge_9 = Part.makeLine(p_7, p_8)
p_10 = FreeCAD.Vector(0, 20.0, 0.0)
p_11 = FreeCAD.Vector(0, 0, 0.0)
edge_12 = Part.makeLine(p_10, p_11)
wire_13 = Part.Wire([edge_3, edge_6, edge_9, edge_12])
face_14 = Part.Face(wire_13)
shape_15 = face_14.extrude(FreeCAD.Vector(0, 0, 10.0))
obj_16 = doc.addObject("Part::Feature", "Extrude")
obj_16.Shape = shape_15
p_17 = FreeCAD.Vector(0, 0, 0.0)
p_18 = FreeCAD.Vector(20.0, 0, 0.0)
edge_19 = Part.makeLine(p_17, p_18)
p_20 = FreeCAD.Vector(20.0, 0, 0.0)
p_21 = FreeCAD.Vector(20.0, 40.0, 0.0)
edge_22 = Part.makeLine(p_20, p_21)
p_23 = FreeCAD.Vector(20.0, 40.0, 0.0)
p_24 = FreeCAD.Vector(0, 40.0, 0.0)
edge_25 = Part.makeLine(p_23, p_24)
p_26 = FreeCAD.Vector(0, 40.0, 0.0)
p_27 = FreeCAD.Vector(0, 0, 0.0)
edge_28 = Part.makeLine(p_26, p_27)
wire_29 = Part.Wire([edge_19, edge_22, edge_25, edge_28])
face_30 = Part.Face(wire_29)
shape_31 = face_30.extrude(FreeCAD.Vector(0, 0, 10.0))
obj_32 = doc.addObject("Part::Feature", "Extrude")
obj_32.Shape = shape_31
shape_33 = obj_16.Shape.fuse(obj_32.Shape)
obj_34 = doc.addObject("Part::Feature", "Union")
obj_34.Shape = shape_33

doc.recompute()

doc.saveAs(r"forge\output\test_union.FCStd")

Import.export([obj_34], r"forge\output\test_union.step")