import numpy as np

from geomosaic.grid import Grid
from geomosaic.hexagrid.hexagon import Hexagon, Orientation
from geomosaic.shape import Shape


class HexagonalGrid(Grid):
    def __init__(
        self,
        width: int,
        height: int,
        size: float,
        margin: int = 2,
        orientation: Orientation = "flat",
    ):
        """Hexagonal (flat-top or pointy-top) grid covering a width x height area.

        Args:
            width (int): width of the area to cover.
            height (int): height of the area to cover.
            size (float): size of the hexagon (radius of the outer circle).
            margin (int, optional): Number of additional rows and columns
            added to the grid dimensions. Defaults to 2.
            orientation (Orientation, optional): "flat" (flat-top) or "pointy" (pointy-top). Defaults to "flat".
        """

        self.orientation = orientation

        super().__init__(width, height, size, margin)

    def _generate(self) -> list[Shape]:
        if self.orientation == "flat":
            x_spacing = 1.5 * self.size
            y_spacing = np.sqrt(3) * self.size
        else:
            x_spacing = np.sqrt(3) * self.size
            y_spacing = 1.5 * self.size

        cols = int(self.width / x_spacing) + self.margin
        rows = int(self.height / y_spacing) + self.margin

        hexagons: list[Shape] = []

        for col in range(cols):
            for row in range(rows):
                cx = col * x_spacing
                cy = row * y_spacing

                if self.orientation == "flat" and col % 2 == 1:
                    cy += y_spacing / 2
                elif self.orientation == "pointy" and row % 2 == 1:
                    cx += x_spacing / 2

                hexagons.append(Hexagon(cx, cy, self.size, self.orientation))

        return hexagons
