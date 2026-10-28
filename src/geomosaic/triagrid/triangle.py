from typing import ClassVar, Literal, get_args

import numpy as np

from geomosaic.shape import Shape

Direction = Literal["up", "down"]


class Triangle(Shape):
    _base_offsets: ClassVar[dict[tuple[float, Direction], np.ndarray]] = {}

    def __init__(self, cx: float, cy: float, size: float, direction: Direction = "up"):
        if direction not in get_args(Direction):
            raise ValueError(f"direction must be 'up' or 'down', received {direction}.")

        self.direction = direction

        super().__init__(cx, cy, size)

    @property
    def width(self) -> float:
        return self.size

    @property
    def height(self) -> float:
        return np.sqrt(3) / 2 * self.size

    @property
    def area(self) -> float:
        return np.sqrt(3) / 4 * self.size**2

    def _compute_edges(self) -> np.ndarray:
        """Compute the coordinates of the edges of one triangle and translate them for the other ones.

        (cx, cy) is the centre of the bounding box, not the centroid of the triangle.

        Returns:
            np.ndarray: An array of shape (3, 2) containing the (x, y) coordinates of the edges.
        """
        key = (self.size, self.direction)

        if key not in self.__class__._base_offsets:
            half_width = self.width / 2
            half_height = self.height / 2

            offsets = np.array(
                [
                    [0.0, -half_height],
                    [-half_width, half_height],
                    [half_width, half_height],
                ]
            )

            if self.direction == "down":
                offsets[:, 1] *= -1

            self.__class__._base_offsets[key] = offsets

        offsets = self.__class__._base_offsets[key]
        return offsets + [self.cx, self.cy]

    def contains_point(self, px: float, py: float) -> bool:
        """Check if a point is in the triangle.

        Args:
            px (float): x coordinate of the point.
            py (float): y coordinate of the point.

        Returns:
            bool: True if the point is in the triangle.
        """
        relative_x = abs(px - self.cx)
        relative_y = py - self.cy

        if self.direction == "down":
            relative_y = -relative_y

        half_height = self.height / 2

        if abs(relative_y) > half_height:
            return False

        return bool(relative_x <= (relative_y + half_height) / np.sqrt(3))
