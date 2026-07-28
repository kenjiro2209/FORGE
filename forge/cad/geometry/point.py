from dataclasses import dataclass

from forge.cad.geometry.vector import Vector


@dataclass(slots=True)
class Point:

    x: float
    y: float
    z: float = 0.0

    def translate(self, vector: Vector):

        return Point(
            self.x + vector.x,
            self.y + vector.y,
            self.z + vector.z,
        )