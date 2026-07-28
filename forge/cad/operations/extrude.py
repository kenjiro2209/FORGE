from forge.cad.sketch.face import Face


class Extrude:

    def __init__(self, face: Face, height: float):
        if height <= 0:
            raise ValueError("Extrusion height must be greater than zero.")
        self.face = face
        self.height = height
        self.obj_var: str | None = None
         
    def build(self, builder):
        edge_vars = [entity.to_edge(builder) for entity in self.face.wire.entities]

        wire_var = builder.next_var("wire")
        builder.add(f"{wire_var} = Part.Wire([{', '.join(edge_vars)}])")

        face_var = builder.next_var("face")
        builder.add(f"{face_var} = Part.Face({wire_var})")

        shape_var = builder.next_var("shape")
        builder.add(f"{shape_var} = {face_var}.extrude(FreeCAD.Vector(0, 0, {self.height}))")

        obj_var = builder.next_var("obj")
        builder.add(f'{obj_var} = doc.addObject("Part::Feature", "Extrude")')
        builder.add(f"{obj_var}.Shape = {shape_var}")

        self.obj_var = obj_var
        return obj_var  