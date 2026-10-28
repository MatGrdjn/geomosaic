from abc import ABC, abstractmethod

import numpy as np


class Shape(ABC):
    def __init__(self, cx: float, cy: float, size: float):
        self.cx = cx
        self.cy = cy
        self.size = size

        self.edges = self._compute_edges()
        self.color: tuple[int, int, int] | None = None

    @property
    def centre(self) -> tuple[float, float]:
        return (self.cx, self.cy)

    @property
    @abstractmethod
    def width(self) -> float:
        """Width of the shape's bounding box."""

    @property
    @abstractmethod
    def height(self) -> float:
        """Height of the shape's bounding box."""

    @property
    @abstractmethod
    def area(self) -> float:
        """Area of the shape."""

    @abstractmethod
    def _compute_edges(self) -> np.ndarray:
        """Compute the coordinates of the vertices of the shape.

        Returns:
            np.ndarray: An array of shape (n, 2) containing the (x, y) coordinates of the vertices.
        """

    @abstractmethod
    def contains_point(self, px: float, py: float) -> bool:
        """Check if a point is in the shape.

        Args:
            px (float): x coordinate of the point.
            py (float): y coordinate of the point.

        Returns:
            bool: True if the point is in the shape.
        """

    def _compute_average_color_random(
        self,
        img_arr: np.ndarray,
        sample_fraction: float = 0.2,
        max_samples: int = 50,
        **kwargs,
    ) -> None:
        """Compute the average color of the shape by randomly drawing pixels.

        The number of samples is dynamically computed based on the shape's area,
        clamped between 5 and `max_samples`.

        Args:
            img_arr (np.ndarray): The image converted in a numpy array, (H, W, C)
            sample_fraction (float, optional): Fraction of total area to sample for small shapes. Defaults to 0.2.
            max_samples (int, optional): Maximum number of random samples. Defaults to 50.
        """
        img_height, img_width = img_arr.shape[:2]

        target_samples = int(self.area * sample_fraction)

        num_samples = max(5, min(target_samples, max_samples))

        color_sum = np.zeros(3, dtype=float)
        valid_points = 0
        attempts = 0
        max_attempts = num_samples * 5  # to avoid infinite loops

        while valid_points < num_samples and attempts < max_attempts:
            attempts += 1

            dx = np.random.uniform(-self.width / 2, self.width / 2)
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

    def _compute_average_color_deterministic(
        self, img_arr: np.ndarray, step: int = 2, **kwargs
    ) -> None:
        """Compute the average color of the shape deterministically
        by scanning a regular pixel grid within its bounding box.

        Args:
            img_arr (np.ndarray): The image converted in a numpy array, (H, W, C).
            step (int, optional): Step size for the grid scan. Defaults to 2.
        """
        img_height, img_width = img_arr.shape[:2]

        x_min = int(max(0, np.floor(self.cx - self.width / 2)))
        x_max = int(min(img_width, np.ceil(self.cx + self.width / 2)))
        y_min = int(max(0, np.floor(self.cy - self.height / 2)))
        y_max = int(min(img_height, np.ceil(self.cy + self.height / 2)))

        color_sum = np.zeros(3, dtype=float)
        valid_points = 0

        for py in range(y_min, y_max, step):
            for px in range(x_min, x_max, step):
                if self.contains_point(float(px), float(py)):
                    color_sum += img_arr[py, px]
                    valid_points += 1

        if valid_points > 0:
            self.color = tuple(np.round(color_sum / valid_points).astype(int))
        else:
            cx_int, cy_int = int(self.cx), int(self.cy)
            if 0 <= cx_int < img_width and 0 <= cy_int < img_height:
                self.color = tuple(img_arr[cy_int, cx_int])
            else:
                self.color = (0, 0, 0)

    def compute_color(
        self, img_arr: np.ndarray, method: str = "deterministic", **kwargs
    ) -> None:
        """Compute the shape color using the specified method.

        Args:
            img_arr (np.ndarray): The image converted in a numpy array, (H, W, C).
            method (str, optional): "deterministic" or "random". Defaults to "deterministic".
            **kwargs: Additional parameters specific to each method.
        """

        if method == "deterministic":
            self._compute_average_color_deterministic(img_arr, **kwargs)
        elif method == "random":
            self._compute_average_color_random(img_arr, **kwargs)
        else:
            raise ValueError(
                f"Unknown sampling method: '{method}'. Use 'deterministic' or 'random'."
            )
