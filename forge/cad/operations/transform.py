from forge.cad.geometry.vector import Vector


class Transform:
    """Aplica una traslacion a otra operacion (Union, Cut, Extrude, etc)."""

    def __init__(self, operation, translation: Vector):
        self.operation = operation
        self.translation = translation
        self.obj_var: str | None = None

    def build(self, builder):
        if self.operation.obj_var is None:
            self.operation.build(builder)

        vector_var = builder.next_var("p")
        placement_var = builder.next_var("placement")

        builder.add(
            f"{vector_var} = FreeCAD.Vector({self.translation.x}, {self.translation.y}, {self.translation.z})"
        )
        builder.add(f"{placement_var} = FreeCAD.Placement({vector_var}, FreeCAD.Rotation())")

        shape_var = builder.next_var("shape")
        builder.add(f"{shape_var} = {self.operation.obj_var}.Shape.copy()")
        builder.add(f"{shape_var}.Placement = {placement_var}")

        obj_var = builder.next_var("obj")
        builder.add(f'{obj_var} = doc.addObject("Part::Feature", "Transform")')
        builder.add(f"{obj_var}.Shape = {shape_var}")

        self.obj_var = obj_var
        return obj_var