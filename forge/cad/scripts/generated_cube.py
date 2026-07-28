import FreeCAD
import Part
import Import

doc = FreeCAD.newDocument("Cube")

cube = Part.makeBox(20, 20, 20)
obj = doc.addObject("Part::Feature", "Cube")
obj.Shape = cube

doc.recompute()

doc.saveAs(r"forge\output\Cube.FCStd")

Import.export([obj], r"forge\output\Cube.step")