from forge.cad.geometry.line import Line


class Sketch:

    def __init__(self):

        self.entities = []

    def add(self, entity):

        self.entities.append(entity)

        return entity

    def lines(self):

        return [
            entity
            for entity in self.entities
            if isinstance(entity, Line)
        ]