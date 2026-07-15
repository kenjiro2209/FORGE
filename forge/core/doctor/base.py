from dataclasses import dataclass


@dataclass
class CheckResult:
    """Resultado de una comprobación del sistema."""

    name: str
    success: bool
    version: str | None = None
    message: str | None = None