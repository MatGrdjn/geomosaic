import marimo

__generated_with = "0.25.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    from dataclasses import dataclass
    from hexagrid.hexagon import generate_hexagonal_grid, Hexagon
    from matplotlib.patches import Polygon
    from PIL import Image

    return Image, Polygon, generate_hexagonal_grid, mo, np, plt


@app.cell
def _(Image, np):
    img_path = "../input/screenshot.jpg"
    img = Image.open(img_path).convert("RGB")
    img_array = np.array(img)
    return img, img_array


@app.cell
def _(img, plt):
    figure, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.imshow(img)
    ax.axis(False)

    plt.show()
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 30, 1, 15, label="hex_size")
    slider
    return (slider,)


@app.cell
def _(Polygon, generate_hexagonal_grid, img, img_array, plt, slider):
    hex_size = int(slider.value)
    grid = generate_hexagonal_grid(width=img.width, height=img.height, size=hex_size)

    for h in grid:
        h.compute_average_color_random(img_array) 

    fig, axes = plt.subplots(figsize=(16, 12))
    axes.set_xlim(0, img.width)
    axes.set_ylim(img.height, 0) 
    axes.set_aspect('equal')
    axes.axis('off') 

    for h in grid:
        if h.color != (0, 0, 0): 
            color_norm = (h.color[0]/255, h.color[1]/255, h.color[2]/255)
        
            poly = Polygon(
                h.edges, 
                closed=True, 
                facecolor=color_norm, 
                edgecolor="white",
                linewidth=0.1
            )
            axes.add_patch(poly)

    plt.show()
    return


if __name__ == "__main__":
    app.run()
