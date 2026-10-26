from pathlib import Path

from geomosaic.hexagrid.hexagon import Hexagon


def export_to_svg(
    grid: list[Hexagon], width: int, height: int, output_path: str | Path
) -> None:
    """
    Exports a grid of hexagons to an SVG file.

    Args:
        grid (list[Hexagon]): List of Hexagon objects with colors.
        width (int): Width of the original image.
        height (int): Height of the original image.
        output_path (str | Path): Path where the .svg file will be saved.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
        )

        for h in grid:
            if h.color is None or h.color == (0, 0, 0):  # OOB hexagons
                continue

            points_str = " ".join([f"{x:.1f},{y:.1f}" for x, y in h.edges])

            r, g, b = h.color

            f.write(f'    <polygon points="{points_str}" fill="rgb({r},{g},{b})" />\n')

        f.write("</svg>\n")
