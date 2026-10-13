"""Geometria de IMAGEM. Unidade: pixels, origem no canto superior esquerdo, y para baixo.

Não existe tipo de coordenada de mundo nesta versão: sem calibração válida, não há metros.
Os valores não são recortados aqui; o adaptador do detector é responsável por normalizar.
"""

from __future__ import annotations

from dataclasses import dataclass

from vyra.domain.checks import ContractError, check_finite


@dataclass(frozen=True, slots=True)
class ImagePoint:
    x: float
    y: float

    def __post_init__(self) -> None:
        check_finite("ImagePoint.x", self.x)
        check_finite("ImagePoint.y", self.y)


@dataclass(frozen=True, slots=True)
class BBox:
    """Caixa alinhada aos eixos, em pixels: (x1, y1) topo-esquerdo, (x2, y2) base-direita."""

    x1: float
    y1: float
    x2: float
    y2: float

    def __post_init__(self) -> None:
        for name in ("x1", "y1", "x2", "y2"):
            check_finite(f"BBox.{name}", getattr(self, name))
        if not (self.x2 > self.x1 and self.y2 > self.y1):
            raise ContractError(
                f"BBox degenerada ou invertida: ({self.x1}, {self.y1}, {self.x2}, {self.y2})"
            )

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center(self) -> ImagePoint:
        return ImagePoint((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    @property
    def bottom_center(self) -> ImagePoint:
        return ImagePoint((self.x1 + self.x2) / 2, self.y2)
