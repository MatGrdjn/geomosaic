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


def generate_hexagonal_grid(
    width: int,
    height: int,
    size: float,
    margin: int = 2,
    orientation: Orientation = "flat",
) -> list[Hexagon]:
    """Generate an hexagonal (flat-top or pointy-top) grid from a classic square grid.

    Args:
        width (int): width of the square grid.
        height (int): height of the square grid.
        size (float): size of the hexagon (radius of the outer circle).
        margin (int, optional):  Number of additional rows and columns
        added to the grid dimensions. Defaults to 2.
        orientation (Orientation, optional): "flat" (flat-top) or "pointy" (pointy-top). Defaults to "flat".

    Returns:
        list[Hexagon]: the hexagonal grid
    """

    if orientation == "flat":
        x_spacing = 1.5 * size
        y_spacing = np.sqrt(3) * size
    else:
        x_spacing = np.sqrt(3) * size
        y_spacing = 1.5 * size

    cols = int(width / x_spacing) + margin
    rows = int(height / y_spacing) + margin

    hexagon_grid = []

    for col in range(cols):
        for row in range(rows):
            cx = col * x_spacing
            cy = row * y_spacing

            if orientation == "flat" and col % 2 == 1:
                cy += y_spacing / 2
            elif orientation == "pointy" and row % 2 == 1:
                cx += x_spacing / 2

            hexagon_grid.append(Hexagon(cx, cy, size, orientation))

    return hexagon_grid
