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