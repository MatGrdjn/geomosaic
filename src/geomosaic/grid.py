from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

import numpy as np

from geomosaic.shape import Shape
from geomosaic.svg import export_to_svg


class Grid(ABC):
    def __init__(self, width: int, height: int, size: float, margin: int = 2):
        self.width = width
        self.height = height
        self.size = size
        self.margin = margin

        self.shapes = self._generate()

    @abstractmethod
    def _generate(self) -> list[Shape]:
        """Generate the shapes covering a width x height area.

        Returns:
            list[Shape]: the shapes of the grid.
        """

    def __len__(self) -> int:
        return len(self.shapes)

    def __iter__(self) -> Iterator[Shape]:
        return iter(self.shapes)

    def compute_colors(
        self, img_arr: np.ndarray, method: str = "deterministic", **kwargs
    ) -> None:
        """Compute the color of every shape of the grid.

        Args:
            img_arr (np.ndarray): The image converted in a numpy array, (H, W, C).
            method (str, optional): "deterministic" or "random". Defaults to "deterministic".
            **kwargs: Additional parameters specific to each method.
        """
        for shape in self.shapes:
            shape.compute_color(img_arr, method=method, **kwargs)

    def to_svg(self, output_path: str | Path) -> None:
        """Export the grid to an SVG file.

        Args:
            output_path (str | Path): Path where the .svg file will be saved.
        """
        export_to_svg(self.shapes, self.width, self.height, output_path)
