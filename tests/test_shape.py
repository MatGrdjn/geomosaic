import numpy as np
import pytest

from geomosaic.hexagrid.hexagon import Hexagon
from geomosaic.shape import Shape


def test_hexagon_is_a_shape():
    assert isinstance(Hexagon(0, 0, 2), Shape)


def test_hexagon_area():
    hexagon = Hexagon(0, 0, 2)

    expected_area = (3 * np.sqrt(3) / 2) * 2**2
    assert hexagon.area == pytest.approx(expected_area)
