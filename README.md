# geomosaic

Turn any image into a mosaic of hexagons or triangles, exported as a vector SVG.

<table>
  <tr>
    <th>Original</th>
    <th>Hexagons</th>
    <th>Triangles</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/MatGrdjn/geomosaic/main/input/example.jpg" alt="Original image" width="280"></td>
    <td><img src="https://raw.githubusercontent.com/MatGrdjn/geomosaic/main/output/example_hexagon.svg" alt="Hexagonal mosaic" width="280"></td>
    <td><img src="https://raw.githubusercontent.com/MatGrdjn/geomosaic/main/output/example_triangle.svg" alt="Triangular mosaic" width="280"></td>
  </tr>
</table>

**[Try it in your browser](https://matgrdjn.github.io/geomosaic/)**, no installation needed.

## Installation

geomosaic requires Python 3.12 or later.

```bash
pip install geomosaic
```

or, in a project managed with [uv](https://docs.astral.sh/uv/):

```bash
uv add geomosaic
```

To use only the command line tool, install it in its own environment:

```bash
uv tool install geomosaic
```

## Command line usage

```bash
# hexagonal mosaic, saved as photo.svg
geomosaic photo.jpg

# triangular mosaic with smaller tiles
geomosaic photo.jpg --shape triangle --size 10 -o mosaic.svg

# pointy-top hexagons
geomosaic photo.jpg --orientation pointy
```

| Option | Default | Description |
|---|---|---|
| `input` | | Image to convert (`.png`, `.jpg`, `.webp`, ...). |
| `-o`, `--output` | `<input>.svg` | Path of the SVG file to create. |
| `--shape` | `hexagon` | Tile shape: `hexagon` or `triangle`. |
| `-s`, `--size` | `15` | Side length of the tiles, in pixels. |
| `--orientation` | `flat` | Hexagons only: `flat` (flat-top) or `pointy` (pointy-top). |
| `-m`, `--margin` | `2` | Extra rows and columns, so the mosaic covers the image edges. |
| `--color-sampling` | `deterministic` | How each tile's color is computed: `deterministic` or `random`. |
| `--step` | `2` | Deterministic sampling: read one pixel every `step` pixels. |
| `--sample-fraction` | `0.2` | Random sampling: fraction of the tile's area to sample. |
| `-v`, `--verbose` | | Print each step. |

## Python usage

```python
import numpy as np
from PIL import Image

from geomosaic.hexagrid import HexagonalGrid
from geomosaic.triagrid import TriangularGrid

img = Image.open("photo.jpg").convert("RGB")
pixels = np.asarray(img)

# hexagons
grid = HexagonalGrid(img.width, img.height, size=15, orientation="pointy")
grid.compute_colors(pixels)
grid.to_svg("hexagons.svg")

# triangles, with random color sampling
grid = TriangularGrid(img.width, img.height, size=15)
grid.compute_colors(pixels, method="random", sample_fraction=0.3)
grid.to_svg("triangles.svg")
```


## How it works

1. A grid of hexagons or triangles is laid over the image, slightly larger than the image so the edges are covered.
2. Each tile takes the average color of the pixels it contains.
3. Each tile is written to the SVG as a `<polygon>`.

## Development

```bash
git clone https://github.com/MatGrdjn/geomosaic.git
cd geomosaic
uv sync

uv run pytest
uv run ruff check .
uv run ruff format .
uv run mypy src
```

## License

MIT
