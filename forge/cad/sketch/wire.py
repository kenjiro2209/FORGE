from forge.cad.sketch.sketch import Sketch


class Wire:

    def __init__(self):

        self._entities = []

    @classmethod
    def from_sketch(cls, sketch: Sketch):

        wire = cls()

        for entity in sketch.entities:
            wire.add(entity)

        return wire

    def add(self, entity):

        self._entities.append(entity)

        return entity

    @property
    def entities(self):

        return tuple(self._entities)