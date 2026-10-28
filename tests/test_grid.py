import numpy as np
import pytest

from geomosaic.hexagrid import Hexagon, HexagonalGrid


@pytest.fixture
def red_image():
    img_arr = np.zeros((100, 100, 3), dtype=int)
    img_arr[:, :] = [255, 0, 0]  # image rouge
    return img_arr


def test_hexagonal_grid_contains_hexagons():
    grid = HexagonalGrid(150, 100, 10, orientation="pointy")

    assert all(isinstance(h, Hexagon) for h in grid)
    assert all(h.orientation == "pointy" for h in grid)


def test_grid_hexagon_count():
    width = 150
    height = 100
    size = 10
    margin = 2

    x_spacing = 1.5 * size
    y_spacing = np.sqrt(3) * size
    expected_cols = int(width / x_spacing) + margin
    expected_rows = int(height / y_spacing) + margin
    expected_total = expected_cols * expected_rows

    grid = HexagonalGrid(width, height, size, margin=margin)
    assert len(grid) == expected_total


def test_grid_hexagon_count_pointy():
    width = 150
    height = 100
    size = 10
    margin = 2

    x_spacing = np.sqrt(3) * size
    y_spacing = 1.5 * size
    expected_cols = int(width / x_spacing) + margin
    expected_rows = int(height / y_spacing) + margin
    expected_total = expected_cols * expected_rows

    grid = HexagonalGrid(width, height, size, margin=margin, orientation="pointy")
    assert len(grid) == expected_total


def test_grid_column_offset():
    size = 10
    grid = HexagonalGrid(width=50, height=50, size=size, margin=0)

    y_spacing = np.sqrt(3) * size
    expected_offset = y_spacing / 2

    hex_col_0 = grid.shapes[0]
    assert hex_col_0.cx == pytest.approx(0.0)
    assert hex_col_0.cy == pytest.approx(0.0)

    x_spacing = 1.5 * size
    hex_col_1 = next(h for h in grid if np.isclose(h.cx, x_spacing))

    assert hex_col_1.cy == pytest.approx(expected_offset)


def test_grid_row_offset_pointy():
    size = 10
    grid = HexagonalGrid(width=50, height=50, size=size, margin=0, orientation="pointy")

    x_spacing = np.sqrt(3) * size
    expected_offset = x_spacing / 2

    hex_row_0 = grid.shapes[0]
    assert hex_row_0.cx == pytest.approx(0.0)
    assert hex_row_0.cy == pytest.approx(0.0)

    y_spacing = 1.5 * size
    hex_row_1 = next(h for h in grid if np.isclose(h.cy, y_spacing))

    assert hex_row_1.cx == pytest.approx(expected_offset)


def test_compute_colors(red_image):
    grid = HexagonalGrid(100, 100, 10)

    grid.compute_colors(red_image)

    assert all(h.color is not None for h in grid)

    inside = [h for h in grid if 0 <= h.cx < 100 and 0 <= h.cy < 100]
    assert all(h.color == (255, 0, 0) for h in inside)


def test_to_svg(tmp_path, red_image):
    grid = HexagonalGrid(100, 100, 10)
    grid.compute_colors(red_image)

    output_file = tmp_path / "grid.svg"
    grid.to_svg(output_file)

    content = output_file.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert "<polygon" in content
