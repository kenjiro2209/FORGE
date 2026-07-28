from typing import List

import typer

from forge.cad.components.rectangle import Rectangle
from forge.cad.freecad_runner import (
    FreeCADExecutionError,
    FreeCADNotFoundError,
    FreeCADTimeoutError,
)
from forge.cad.geometry.circle import Circle
from forge.cad.geometry.point import Point
from forge.cad.geometry.vector import Vector
from forge.cad.model import Model
from forge.cad.operations.chamfer import Chamfer
from forge.cad.operations.cut import Cut
from forge.cad.operations.extrude import Extrude
from forge.cad.operations.fillet import Fillet
from forge.cad.operations.intersection import Intersection
from forge.cad.operations.transform import Transform
from forge.cad.operations.union import Union
from forge.cad.service import build as build_model
from forge.cad.sketch.face import Face
from forge.cad.sketch.sketch import Sketch
from forge.cad.sketch.wire import Wire

app = typer.Typer(help="Comandos CAD basados en FreeCAD")

FORMAT_OPTION = typer.Option(
    ["step"],
    "--format",
    "-f",
    help=(
        "Formato(s) de exportacion: step, iges, stl, obj, dxf, svg. "
        "Repetible (-f step -f stl)."
    ),
)


def _run_and_report(name: str, model: Model, formats: List[str], label: str = "generado"):
    """Ejecuta el build de un modelo y reporta el resultado al usuario.

    Centraliza el manejo de errores de FreeCAD para que todos los
    comandos se comporten igual ante un fallo.
    """

    try:
        build_model(model, formats=tuple(formats))
    except FreeCADNotFoundError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    except FreeCADTimeoutError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    except FreeCADExecutionError as exc:
        typer.echo(f"Error al ejecutar FreeCAD:\n{exc.stderr}", err=True)
        raise typer.Exit(code=1)

    formats_str = ", ".join(formats)
    typer.echo(
        f"Modelo '{name}' ({label}) generado correctamente en forge/output/ "
        f"[{formats_str}]"
    )


def _build_extrude(width: float, height: float, depth: float) -> Extrude:
    rectangle = Rectangle(width=width, height=height)
    sketch = rectangle.build()
    wire = Wire.from_sketch(sketch)
    face = Face(wire)
    return Extrude(face=face, height=depth)


def _build_cylinder(radius: float, depth: float) -> Extrude:
    sketch = Sketch()
    sketch.add(Circle(center=Point(0, 0), radius=radius))
    wire = Wire.from_sketch(sketch)
    face = Face(wire)
    return Extrude(face=face, height=depth)


@app.command()
def extrude(
    name: str = typer.Option("model", help="Nombre del modelo generado."),
    width: float = typer.Option(..., help="Ancho del rectangulo base (mm)."),
    height: float = typer.Option(..., help="Alto del rectangulo base (mm)."),
    depth: float = typer.Option(..., help="Altura de extrusion (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Genera un solido extruyendo un rectangulo parametrico."""

    operation = _build_extrude(width, height, depth)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format)


@app.command()
def cylinder(
    name: str = typer.Option("cylinder", help="Nombre del modelo generado."),
    radius: float = typer.Option(..., help="Radio del circulo base (mm)."),
    depth: float = typer.Option(..., help="Altura de extrusion (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Genera un cilindro extruyendo un circulo parametrico."""

    operation = _build_cylinder(radius, depth)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format)


@app.command()
def union(
    name: str = typer.Option("union_model", help="Nombre del modelo generado."),
    width_a: float = typer.Option(..., help="Ancho de la primera pieza (mm)."),
    height_a: float = typer.Option(..., help="Alto de la primera pieza (mm)."),
    depth_a: float = typer.Option(..., help="Extrusion de la primera pieza (mm)."),
    width_b: float = typer.Option(..., help="Ancho de la segunda pieza (mm)."),
    height_b: float = typer.Option(..., help="Alto de la segunda pieza (mm)."),
    depth_b: float = typer.Option(..., help="Extrusion de la segunda pieza (mm)."),
    offset_x: float = typer.Option(0, help="Desplazamiento en X de la segunda pieza (mm)."),
    offset_y: float = typer.Option(0, help="Desplazamiento en Y de la segunda pieza (mm)."),
    offset_z: float = typer.Option(0, help="Desplazamiento en Z de la segunda pieza (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Une (fuse) dos solidos extruidos, con posicionamiento opcional."""

    base = _build_extrude(width_a, height_a, depth_a)
    tool = _build_extrude(width_b, height_b, depth_b)

    if offset_x or offset_y or offset_z:
        tool = Transform(tool, translation=Vector(offset_x, offset_y, offset_z))

    operation = Union(base=base, tool=tool)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format, label="union")


@app.command()
def cut(
    name: str = typer.Option("cut_model", help="Nombre del modelo generado."),
    width_a: float = typer.Option(..., help="Ancho de la pieza base (mm)."),
    height_a: float = typer.Option(..., help="Alto de la pieza base (mm)."),
    depth_a: float = typer.Option(..., help="Extrusion de la pieza base (mm)."),
    width_b: float = typer.Option(..., help="Ancho de la herramienta de corte (mm)."),
    height_b: float = typer.Option(..., help="Alto de la herramienta de corte (mm)."),
    depth_b: float = typer.Option(..., help="Extrusion de la herramienta de corte (mm)."),
    offset_x: float = typer.Option(0, help="Desplazamiento en X de la herramienta (mm)."),
    offset_y: float = typer.Option(0, help="Desplazamiento en Y de la herramienta (mm)."),
    offset_z: float = typer.Option(0, help="Desplazamiento en Z de la herramienta (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Resta (cut) una pieza de otra, con posicionamiento opcional."""

    base = _build_extrude(width_a, height_a, depth_a)
    tool = _build_extrude(width_b, height_b, depth_b)

    if offset_x or offset_y or offset_z:
        tool = Transform(tool, translation=Vector(offset_x, offset_y, offset_z))

    operation = Cut(base=base, tool=tool)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format, label="cut")


@app.command()
def intersection(
    name: str = typer.Option("intersection_model", help="Nombre del modelo generado."),
    width_a: float = typer.Option(..., help="Ancho de la primera pieza (mm)."),
    height_a: float = typer.Option(..., help="Alto de la primera pieza (mm)."),
    depth_a: float = typer.Option(..., help="Extrusion de la primera pieza (mm)."),
    width_b: float = typer.Option(..., help="Ancho de la segunda pieza (mm)."),
    height_b: float = typer.Option(..., help="Alto de la segunda pieza (mm)."),
    depth_b: float = typer.Option(..., help="Extrusion de la segunda pieza (mm)."),
    offset_x: float = typer.Option(0, help="Desplazamiento en X de la segunda pieza (mm)."),
    offset_y: float = typer.Option(0, help="Desplazamiento en Y de la segunda pieza (mm)."),
    offset_z: float = typer.Option(0, help="Desplazamiento en Z de la segunda pieza (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Interseca (common) dos solidos extruidos, con posicionamiento opcional."""

    base = _build_extrude(width_a, height_a, depth_a)
    tool = _build_extrude(width_b, height_b, depth_b)

    if offset_x or offset_y or offset_z:
        tool = Transform(tool, translation=Vector(offset_x, offset_y, offset_z))

    operation = Intersection(base=base, tool=tool)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format, label="interseccion")


@app.command()
def fillet(
    name: str = typer.Option("fillet_model", help="Nombre del modelo generado."),
    width: float = typer.Option(..., help="Ancho del rectangulo base (mm)."),
    height: float = typer.Option(..., help="Alto del rectangulo base (mm)."),
    depth: float = typer.Option(..., help="Altura de extrusion (mm)."),
    radius: float = typer.Option(..., help="Radio del redondeo (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Genera un solido extruido con los edges redondeados (fillet)."""

    base = _build_extrude(width, height, depth)
    operation = Fillet(base, radius=radius)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format, label="fillet")


@app.command()
def chamfer(
    name: str = typer.Option("chamfer_model", help="Nombre del modelo generado."),
    width: float = typer.Option(..., help="Ancho del rectangulo base (mm)."),
    height: float = typer.Option(..., help="Alto del rectangulo base (mm)."),
    depth: float = typer.Option(..., help="Altura de extrusion (mm)."),
    distance: float = typer.Option(..., help="Distancia del chaflan (mm)."),
    format: List[str] = FORMAT_OPTION,
):
    """Genera un solido extruido con los edges achaflanados (chamfer)."""

    base = _build_extrude(width, height, depth)
    operation = Chamfer(base, distance=distance)

    model = Model(name)
    model.add(operation)

    _run_and_report(name, model, formats=format, label="chamfer")