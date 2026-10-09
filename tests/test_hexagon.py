import numpy as np
import pytest

from hexagrid.hexagon import Hexagon


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

    expected_x = 1.0    # size / 2
    expected_y = np.sqrt(3) # (sqrt(3) / 2) * size
    assert hexagon.edges[1][0] == pytest.approx(expected_x)
    assert hexagon.edges[1][1] == pytest.approx(expected_y)