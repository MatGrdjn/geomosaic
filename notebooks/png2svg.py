import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    from dataclasses import dataclass
    from PIL import Image

    return Image, mo, np, plt


@app.cell
def _(Image):
    image = Image.open("../input/screenshot.jpg")
    return (image,)


@app.cell
def _(image, plt):
    figure, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.imshow(image)
    ax.axis(False)

    plt.show()
    return


@app.cell
def _(image, np):
    img = np.array(image)
    return


@app.cell
def _(np):
    class Hexagon:
        def __init__(self, cx: int | float, cy: int | float, size: int | float):
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

    return (Hexagon,)


@app.cell
def _(Hexagon, np):
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

    return


@app.cell
def _(mo):
    slider = mo.ui.slider(start=1, stop=20, step=1, value=1, label="size", show_value=True)
    slider
    return


if __name__ == "__main__":
    app.run()
