from forge.cad.geometry.point import Point
from forge.cad.geometry.line import Line
from forge.cad.sketch.sketch import Sketch


class Rectangle:

    def __init__(self, width: float, height: float):

        self.width = width
        self.height = height

    def build(self):

        sketch = Sketch()

        p1 = Point(0, 0)
        p2 = Point(self.width, 0)
        p3 = Point(self.width, self.height)
        p4 = Point(0, self.height)

        sketch.add(Line(p1, p2))
        sketch.add(Line(p2, p3))
        sketch.add(Line(p3, p4))
        sketch.add(Line(p4, p1))

        return sketch