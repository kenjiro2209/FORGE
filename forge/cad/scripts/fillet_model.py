import FreeCAD
import Part
import Import

doc = FreeCAD.newDocument("fillet_model")

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
shape_17 = obj_16.Shape.makeFillet(3.0, obj_16.Shape.Edges)
obj_18 = doc.addObject("Part::Feature", "Fillet")
obj_18.Shape = shape_17

doc.recompute()

doc.saveAs(r"forge\output\fillet_model.FCStd")

Import.export([obj_18], r"forge\output\fillet_model.step")