from forge.cad.sketch.wire import Wire


class Face:

    def __init__(self, wire: Wire):

        if len(wire.entities) == 0:
            raise ValueError(
                "A face requires at least one entity."
            )

        self.wire = wire