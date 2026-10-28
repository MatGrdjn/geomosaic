from typing import ClassVar, Literal, get_args

import numpy as np

from geomosaic.shape import Shape

Orientation = Literal["flat", "pointy"]


class Hexagon(Shape):
    _base_offsets: ClassVar[dict[tuple[float, Orientation], np.ndarray]] = {}

    def __init__(
        self, cx: float, cy: float, size: float, orientation: Orientation = "flat"
    ):
        if orientation not in get_args(Orientation):
            raise ValueError(
                f"orientation must be 'flat' or 'pointy', received {orientation}."
            )

        self.orientation = orientation

        super().__init__(cx, cy, size)

    @property
    def height(self) -> float:
        if self.orientation == "flat":
            return np.sqrt(3) * self.size
        else:
            return 2 * self.size

    @property
    def width(self) -> float:
        if self.orientation == "flat":
            return 2 * self.size
        else:
            return np.sqrt(3) * self.size

    @property
    def area(self) -> float:
        return (3 * np.sqrt(3) / 2) * self.size**2

    def _compute_edges(self) -> np.ndarray:
        """Compute the coordinates of the edges of one hexagon and translate them for the other ones.

        Returns:
            np.ndarray: An array of shape (6, 2) containing the (x, y) coordinates of the edges.
        """
        key = (self.size, self.orientation)

        if key not in self.__class__._base_offsets:
            angle_offset = 0 if self.orientation == "flat" else 30
            angles_rad = np.radians(60 * np.arange(6) + angle_offset)

            dx = self.size * np.cos(angles_rad)
            dy = self.size * np.sin(angles_rad)

            self.__class__._base_offsets[key] = np.column_stack((dx, dy))

        offsets = self.__class__._base_offsets[key]
        return offsets + [self.cx, self.cy]

    def contains_point(self, px: float, py: float) -> bool:
        """Check if a point is in the hexagon.

        Args:
            px (float): x coordinate of the point.
            py (float): y coordinate of the point.

        Returns:
            bool: True is the point is in the hexagon.
        """
        relative_x = abs(px - self.cx)
        relative_y = abs(py - self.cy)

        if self.orientation == "pointy":
            relative_x, relative_y = relative_y, relative_x

        if relative_y > np.sqrt(3) / 2 * self.size:
            return False

        return bool((np.sqrt(3) * relative_x + relative_y) <= (np.sqrt(3) * self.size))
