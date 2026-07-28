from dataclasses import dataclass

from forge.cad.geometry.point import Point


@dataclass(slots=True)
class Circle:
    center: Point
    radius: float

    def __post_init__(self):
        if self.radius <= 0:
            raise ValueError("Circle radius must be greater than zero.")

    def to_edge(self, builder) -> str:
        center_var = builder.next_var("p")
        edge_var = builder.next_var("edge")

        builder.add(f"{center_var} = FreeCAD.Vector({self.center.x}, {self.center.y}, {self.center.z})")
        builder.add(f"{edge_var} = Part.makeCircle({self.radius}, {center_var})")

        return edge_var