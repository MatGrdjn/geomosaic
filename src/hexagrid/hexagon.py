import numpy as np


class Hexagon:
    def __init__(self, cx: float, cy: float, size: float):
        self.cx = cx
        self.cy = cy
        self.size = size

        self.edges = self._compute_edges()
    
    @property
    def height(self):
        return np.sqrt(3) * self.size

    @property
    def width(self):
        return 2 * self.size

    @property
    def centre(self):
        return (self.cx, self.cy)
    

    def _compute_edges(self):

        edges = []
        for i in range(6):
            angle_rad = np.radians(60 * i)

            px = self.size * np.cos(angle_rad) + self.cx
            py = self.size * np.sin(angle_rad) + self.cy

            edges.append([px, py])

        return edges


def generate_hexagonal_grid(width: int, height: int, size: int, margin: int = 2) -> list[Hexagon]:

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