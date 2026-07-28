class Union:
    """Combina dos operaciones (booleana: fuse) en un solo sólido."""

    def __init__(self, base, tool):
        self.base = base
        self.tool = tool
        self.obj_var: str | None = None

    def build(self, builder):
        # Construye las dos operaciones de entrada si aún no se han construido.
        if self.base.obj_var is None:
            self.base.build(builder)
        if self.tool.obj_var is None:
            self.tool.build(builder)

        shape_var = builder.next_var("shape")
        builder.add(
            f"{shape_var} = {self.base.obj_var}.Shape.fuse({self.tool.obj_var}.Shape)"
        )

        obj_var = builder.next_var("obj")
        builder.add(f'{obj_var} = doc.addObject("Part::Feature", "Union")')
        builder.add(f"{obj_var}.Shape = {shape_var}")

        self.obj_var = obj_var
        return obj_var