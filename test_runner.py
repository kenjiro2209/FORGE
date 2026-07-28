from forge.cad.components.rectangle import Rectangle
from forge.cad.freecad_runner import FreeCADNotFoundError
from forge.cad.model import Model
from forge.cad.operations.extrude import Extrude
from forge.cad.service import build
from forge.cad.sketch.face import Face
from forge.cad.sketch.wire import Wire


def main():

    rectangle = Rectangle(
        width=40,
        height=20,
    )

    sketch = rectangle.build()
    wire = Wire.from_sketch(sketch)
    face = Face(wire)

    extrude = Extrude(
        face=face,
        height=10,
    )

    model = Model("rectangle_test")
    model.add(extrude)

    print("===== FORGE MODEL =====")
    print(f"Model: {model.name}")
    print(f"Operations: {len(model.operations)}")
    print(f"Operation: {type(model.operations[0]).__name__}")
    print(f"Height: {model.operations[0].height} mm")

    try:
        result = build(model)
    except FreeCADNotFoundError as error:
        print(f"\n[AVISO] {error}")
        return

    print("\n===== FREECAD RUN =====")
    print(f"Return code: {result.returncode}")

    if result.returncode != 0:
        print(result.stderr)
    else:
        print("Modelo generado en forge/output/")


if __name__ == "__main__":
    main()
