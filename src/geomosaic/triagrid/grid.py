import numpy as np

from geomosaic.grid import Grid
from geomosaic.shape import Shape
from geomosaic.triagrid.triangle import Direction, Triangle


class TriangularGrid(Grid):
    """Grid of equilateral triangles, alternately pointing up and down, covering a width x height area."""

    def _generate(self) -> list[Shape]:
        x_spacing = self.size / 2
        y_spacing = np.sqrt(3) / 2 * self.size

        cols = int(self.width / x_spacing) + self.margin
        rows = int(self.height / y_spacing) + self.margin

        triangles: list[Shape] = []

        for col in range(cols):
            for row in range(rows):
                cx = col * x_spacing
                cy = row * y_spacing

                direction: Direction = "up" if (col + row) % 2 == 0 else "down"

                triangles.append(Triangle(cx, cy, self.size, direction))

        return triangles
