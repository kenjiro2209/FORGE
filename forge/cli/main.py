import typer

from forge.core.version import VERSION

app = typer.Typer(
    help="Forge - AI Engineering Platform"
)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show Forge version."
    )
):
    if version:
        typer.echo(f"Forge {VERSION}")
        raise typer.Exit()
    
    
from rich.console import Console

from forge.core.doctor import run

console = Console()


@app.command()
def doctor():
    """Check the development environment."""

    console.print("[bold cyan]Forge Doctor[/bold cyan]\n")

    for result in run():
        icon = "✔" if result.success else "✘"

        version = f" ({result.version})" if result.version else ""

        console.print(f"{icon} {result.name}{version}")