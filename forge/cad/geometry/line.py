from dataclasses import dataclass

from forge.cad.geometry.point import Point
from forge.cad.geometry.vector import Vector


@dataclass(slots=True)
class Line:
    start: Point
    end: Point

    def vector(self) -> Vector:
        return Vector(
            self.end.x - self.start.x,
            self.end.y - self.start.y,
            self.end.z - self.start.z,
        )

    def length(self) -> float:
        return self.vector().length()

    def midpoint(self) -> Point:
        return Point(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
            (self.start.z + self.end.z) / 2,
        )

    def direction(self) -> Vector:
        return self.vector().normalized()

    def to_edge(self, builder) -> str:
        """Genera el edge de FreeCAD y devuelve el nombre de variable."""
        p1_var = builder.next_var("p")
        p2_var = builder.next_var("p")
        edge_var = builder.next_var("edge")

        builder.add(f"{p1_var} = FreeCAD.Vector({self.start.x}, {self.start.y}, {self.start.z})")
        builder.add(f"{p2_var} = FreeCAD.Vector({self.end.x}, {self.end.y}, {self.end.z})")
        builder.add(f"{edge_var} = Part.makeLine({p1_var}, {p2_var})")

        return edge_var