from typing import ClassVar

import numpy as np


class Hexagon:
    _base_offsets: ClassVar[dict[float, np.ndarray]] = {}

    def __init__(self, cx: float, cy: float, size: float):
        self.cx = cx
        self.cy = cy
        self.size = size

        self.edges = self._compute_edges()
        self.color: tuple[int, int, int] | None = None

    @property
    def height(self):
        return np.sqrt(3) * self.size

    @property
    def width(self):
        return 2 * self.size

    @property
    def centre(self):
        return (self.cx, self.cy)

    def _compute_edges(self) -> np.ndarray:
        """Compute the coordinates of the edges of one hexagon and translate them for the other ones.

        Returns:
            np.ndarray: An array of shape (6, 2) containing the (x, y) coordinates of the edges.
        """
        if self.size not in self.__class__._base_offsets:
            angles_rad = np.radians(60 * np.arange(6))

            dx = self.size * np.cos(angles_rad)
            dy = self.size * np.sin(angles_rad)

            self.__class__._base_offsets[self.size] = np.column_stack((dx, dy))

        offsets = self.__class__._base_offsets[self.size]
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

        if relative_y > self.height / 2:
            return False

        return bool((np.sqrt(3) * relative_x + relative_y) <= (np.sqrt(3) * self.size))

    def compute_average_color_random(
        self, img_arr: np.ndarray, sample_fraction: float = 0.2, max_samples: int = 50
    ) -> None:
        """Compute the average color of the hexagon by randomly drawing pixels.

        The number of samples is dynamically computed based on the hexagon's area,
        clamped between 5 and `max_samples` to have a trade-off between both speed and accuracy.

        Args:
            img_arr (np.ndarray): The image converted in a numpy array, (H, W, C)
            sample_fraction (float, optional): Fraction of total area to sample for small hexagons. Defaults to 0.2.
            max_samples (int, optional): Maximum number of random samples. Defaults to 50.
        """
        img_height, img_width = img_arr.shape[:2]

        approx_area = (3 * np.sqrt(3) / 2) * (self.size**2)
        target_samples = int(approx_area * sample_fraction)

        num_samples = max(5, min(target_samples, max_samples))

        color_sum = np.zeros(3, dtype=float)
        valid_points = 0
        attempts = 0
        max_attempts = num_samples * 5  # to avoid infinite loops

        while valid_points < num_samples and attempts < max_attempts:
            attempts += 1

            dx = np.random.uniform(-self.size, self.size)
            dy = np.random.uniform(-self.height / 2, self.height / 2)

            if self.contains_point(self.cx + dx, self.cy + dy):
                px, py = int(self.cx + dx), int(self.cy + dy)

                if 0 <= px < img_width and 0 <= py < img_height:
                    color_sum += img_arr[py, px]
                    valid_points += 1

        if valid_points > 0:
            self.color = tuple(np.round(color_sum / valid_points).astype(int))
        else:
            self.color = (0, 0, 0)


def generate_hexagonal_grid(
    width: int, height: int, size: float, margin: int = 2
) -> list[Hexagon]:
    """Generate a flat-top hexagonal grid from a classic square grid.

    Args:
        width (int): width of the square grid.
        height (int): height of the square grid.
        size (float): size of the flat-top hexagon (radius of the outer circle).
        margin (int, optional):  Number of additional rows and columns
        added to the grid dimensions. Defaults to 2.

    Returns:
        list[Hexagon]: the hexagonal grid
    """

    x_spacing = 1.5 * size
    y_spacing = np.sqrt(3) * size

    cols = int(width / x_spacing) + margin
    rows = int(height / y_spacing) + margin

    hexagon_grid = []

    for col in range(cols):
        y_offset = y_spacing / 2 if (col % 2 == 1) else 0

        for row in range(rows):
            cx = col * x_spacing
            cy = row * y_spacing + y_offset

            hexagon_grid.append(Hexagon(cx, cy, size))

    return hexagon_grid
