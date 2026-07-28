class Cube:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.obj_var: str | None = None

    def build(self, builder):
        shape_var = builder.next_var("shape")
        obj_var = builder.next_var("obj")

        builder.add(f"{shape_var} = Part.makeBox({self.x}, {self.y}, {self.z})")
        builder.add(f'{obj_var} = doc.addObject("Part::Feature", "Cube")')
        builder.add(f"{obj_var}.Shape = {shape_var}")

        self.obj_var = obj_var
        return obj_var