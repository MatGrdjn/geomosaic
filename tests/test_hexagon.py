import numpy as np
import pytest

from hexagrid.hexagon import Hexagon, generate_hexagonal_grid


def test_initialization():
    hexagon = Hexagon(0, 0, 2)

    assert hexagon.cx == 0
    assert hexagon.cy == 0
    assert hexagon.centre == (0, 0)
    assert hexagon.size == 2


def test_dimensions():
    hexagon = Hexagon(0, 0, 2)

    assert hexagon.width == 4

    expected_height = np.sqrt(3) * 2
    assert hexagon.height == pytest.approx(expected_height)


def test_hexagon_edges():

    hexagon = Hexagon(0, 0, 2)

    assert len(hexagon.edges) == 6
    assert len(hexagon.edges[0]) == 2

    assert hexagon.edges[0][0] == pytest.approx(2.0)
    assert hexagon.edges[0][1] == pytest.approx(0.0)

    expected_x = 1.0  # size / 2
    expected_y = np.sqrt(3)  # (sqrt(3) / 2) * size
    assert hexagon.edges[1][0] == pytest.approx(expected_x)
    assert hexagon.edges[1][1] == pytest.approx(expected_y)


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

    grid = generate_hexagonal_grid(width, height, size, margin=margin)
    assert len(grid) == expected_total


def test_grid_column_offset():
    size = 10
    grid = generate_hexagonal_grid(width=50, height=50, size=size, margin=0)

    y_spacing = np.sqrt(3) * size
    expected_offset = y_spacing / 2

    hex_col_0 = grid[0]
    assert hex_col_0.cx == pytest.approx(0.0)
    assert hex_col_0.cy == pytest.approx(0.0)

    x_spacing = 1.5 * size
    hex_col_1 = next(h for h in grid if np.isclose(h.cx, x_spacing))

    assert hex_col_1.cy == pytest.approx(expected_offset)
