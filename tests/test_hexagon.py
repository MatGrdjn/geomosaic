import numpy as np
import pytest

from geomosaic.hexagrid import Hexagon

ORIENTATIONS = ["flat", "pointy"]


@pytest.fixture
def flat_hexagon():
    return Hexagon(0, 0, 2)


@pytest.fixture
def pointy_hexagon():
    return Hexagon(0, 0, 2, orientation="pointy")


@pytest.fixture(params=ORIENTATIONS)
def hexagon(request):
    return Hexagon(0, 0, 2, orientation=request.param)


@pytest.fixture(params=ORIENTATIONS)
def color_hexagon(request):
    return Hexagon(cx=5.0, cy=5.0, size=4.0, orientation=request.param)


@pytest.fixture
def red_image():
    img_arr = np.zeros((100, 100, 3), dtype=int)
    img_arr[:, :] = [255, 0, 0]  # image rouge
    return img_arr


def test_initialization(hexagon):
    assert hexagon.cx == 0
    assert hexagon.cy == 0
    assert hexagon.centre == (0, 0)
    assert hexagon.size == 2


def test_default_orientation(flat_hexagon):
    assert flat_hexagon.orientation == "flat"


def test_invalid_orientation():
    with pytest.raises(ValueError):
        Hexagon(0, 0, 2, orientation="diagonal")


def test_dimensions(flat_hexagon):
    assert flat_hexagon.width == 4

    expected_height = np.sqrt(3) * 2
    assert flat_hexagon.height == pytest.approx(expected_height)


def test_dimensions_pointy(pointy_hexagon):
    expected_width = np.sqrt(3) * 2
    assert pointy_hexagon.width == pytest.approx(expected_width)

    assert pointy_hexagon.height == 4


def test_hexagon_edges(flat_hexagon):
    assert len(flat_hexagon.edges) == 6
    assert len(flat_hexagon.edges[0]) == 2

    assert flat_hexagon.edges[0][0] == pytest.approx(2.0)
    assert flat_hexagon.edges[0][1] == pytest.approx(0.0)

    expected_x = 1.0  # size / 2
    expected_y = np.sqrt(3)  # (sqrt(3) / 2) * size
    assert flat_hexagon.edges[1][0] == pytest.approx(expected_x)
    assert flat_hexagon.edges[1][1] == pytest.approx(expected_y)


def test_hexagon_edges_pointy(pointy_hexagon):
    assert len(pointy_hexagon.edges) == 6
    assert len(pointy_hexagon.edges[0]) == 2

    expected_x = np.sqrt(3)  # (sqrt(3) / 2) * size
    expected_y = 1.0  # size / 2
    assert pointy_hexagon.edges[0][0] == pytest.approx(expected_x)
    assert pointy_hexagon.edges[0][1] == pytest.approx(expected_y)

    assert pointy_hexagon.edges[1][0] == pytest.approx(0.0)
    assert pointy_hexagon.edges[1][1] == pytest.approx(2.0)


def test_edges_distance_to_centre(hexagon):
    distances = np.linalg.norm(hexagon.edges - hexagon.centre, axis=1)

    assert distances == pytest.approx(np.full(6, hexagon.size))


def test_base_offsets_cache_per_orientation(flat_hexagon, pointy_hexagon):
    assert not np.allclose(flat_hexagon.edges, pointy_hexagon.edges)


def test_hexagon_contains_point():
    h = Hexagon(cx=10, cy=10, size=10)

    assert h.contains_point(10, 10) is True

    assert h.contains_point(12, 12) is True

    assert h.contains_point(10, 10 + h.height) is False

    assert h.contains_point(10 + h.size * 2, 10) is False


def test_hexagon_contains_point_pointy():
    h = Hexagon(cx=10, cy=10, size=10, orientation="pointy")

    assert h.contains_point(10, 10) is True

    assert h.contains_point(12, 12) is True

    assert h.contains_point(10, 10 + 9.9) is True

    assert h.contains_point(10 + 9.5, 10) is False

    assert h.contains_point(10, 10 + h.height) is False


def test_compute_average_color_random(color_hexagon, red_image):
    color_hexagon._compute_average_color_random(red_image)

    assert color_hexagon.color == (255, 0, 0)


def test_compute_average_color_determinsitic(color_hexagon, red_image):
    color_hexagon._compute_average_color_deterministic(red_image)

    assert color_hexagon.color == (255, 0, 0)


@pytest.mark.parametrize("orientation", ORIENTATIONS)
def test_compute_color_is_deterministic(orientation):
    img = np.random.randint(0, 256, (100, 100, 3), dtype=int)

    hex1 = Hexagon(cx=5.0, cy=5.0, size=4.0, orientation=orientation)
    hex2 = Hexagon(cx=5.0, cy=5.0, size=4.0, orientation=orientation)

    hex1.compute_color(img, method="deterministic")
    hex2.compute_color(img, method="deterministic")

    assert hex1.color == hex2.color


def test_compute_color_invalid_method(color_hexagon):
    img = np.zeros((100, 100, 3), dtype=int)

    with pytest.raises(ValueError):
        color_hexagon.compute_color(img, method="unknown_method")
