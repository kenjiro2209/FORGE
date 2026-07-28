from __future__ import annotations


class Fillet:
    """Aplica un redondeo (fillet) a los edges de otra operación
    (Extrude, Union, Cut, etc).

    Si no se especifican `edges`, el redondeo se aplica a todos los
    edges del sólido resultante.
    """

    def __init__(self, operation, radius: float, edges: list[int] | None = None):
        if radius <= 0:
            raise ValueError("Fillet radius must be greater than zero.")

        self.operation = operation
        self.radius = radius
        self.edges = edges
        self.obj_var: str | None = None

    def build(self, builder):
        if self.operation.obj_var is None:
            self.operation.build(builder)

        base_var = self.operation.obj_var

        if self.edges is None:
            edges_expr = f"{base_var}.Shape.Edges"
        else:
            indices = ", ".join(str(i) for i in self.edges)
            edges_expr = f"[{base_var}.Shape.Edges[i] for i in ({indices},)]"

        shape_var = builder.next_var("shape")
        builder.add(
            f"{shape_var} = {base_var}.Shape.makeFillet({self.radius}, {edges_expr})"
        )

        obj_var = builder.next_var("obj")
        builder.add(f'{obj_var} = doc.addObject("Part::Feature", "Fillet")')
        builder.add(f"{obj_var}.Shape = {shape_var}")

        self.obj_var = obj_var
        return obj_var