from dataclasses import dataclass
import math


@dataclass(slots=True)
class Vector:

    x: float
    y: float
    z: float = 0.0

    def length(self) -> float:
        return math.sqrt(
            self.x**2 +
            self.y**2 +
            self.z**2
        )

    def normalized(self):

        l = self.length()

        return Vector(
            self.x / l,
            self.y / l,
            self.z / l
        )