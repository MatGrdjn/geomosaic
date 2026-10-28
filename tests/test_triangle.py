import numpy as np
import pytest

from geomosaic.shape import Shape
from geomosaic.triagrid import Triangle

DIRECTIONS = ["up", "down"]


@pytest.fixture
def up_triangle():
    return Triangle(0, 0, 2)


@pytest.fixture
def down_triangle():
    return Triangle(0, 0, 2, direction="down")


@pytest.fixture(params=DIRECTIONS)
def triangle(request):
    return Triangle(0, 0, 2, direction=request.param)


@pytest.fixture(params=DIRECTIONS)
def color_triangle(request):
    return Triangle(cx=5.0, cy=5.0, size=4.0, direction=request.param)


@pytest.fixture
def red_image():
    img_arr = np.zeros((100, 100, 3), dtype=int)
    img_arr[:, :] = [255, 0, 0]  # image rouge
    return img_arr


def test_initialization(triangle):
    assert triangle.cx == 0
    assert triangle.cy == 0
    assert triangle.centre == (0, 0)
    assert triangle.size == 2


def test_triangle_is_a_shape(triangle):
    assert isinstance(triangle, Shape)


def test_default_direction(up_triangle):
    assert up_triangle.direction == "up"


def test_invalid_direction():
    with pytest.raises(ValueError):
        Triangle(0, 0, 2, direction="left")


def test_dimensions(triangle):
    assert triangle.width == 2

    expected_height = np.sqrt(3)  # (sqrt(3) / 2) * size
    assert triangle.height == pytest.approx(expected_height)

    expected_area = np.sqrt(3)  # (sqrt(3) / 4) * size**2
    assert triangle.area == pytest.approx(expected_area)


def test_triangle_edges_up(up_triangle):
    assert len(up_triangle.edges) == 3
    assert len(up_triangle.edges[0]) == 2

    half_height = np.sqrt(3) / 2

    assert up_triangle.edges[0][0] == pytest.approx(0.0)
    assert up_triangle.edges[0][1] == pytest.approx(-half_height)

    assert up_triangle.edges[1][0] == pytest.approx(-1.0)
    assert up_triangle.edges[1][1] == pytest.approx(half_height)
    assert up_triangle.edges[2][0] == pytest.approx(1.0)
    assert up_triangle.edges[2][1] == pytest.approx(half_height)


def test_triangle_edges_down(down_triangle):
    assert len(down_triangle.edges) == 3

    half_height = np.sqrt(3) / 2

    assert down_triangle.edges[0][0] == pytest.approx(0.0)
    assert down_triangle.edges[0][1] == pytest.approx(half_height)

    assert down_triangle.edges[1][1] == pytest.approx(-half_height)
    assert down_triangle.edges[2][1] == pytest.approx(-half_height)


def test_triangle_contains_point_up():
    t = Triangle(cx=10, cy=10, size=10)

    assert t.contains_point(10, 10) is True

    assert t.contains_point(10, 10 - 4.2) is True

    assert t.contains_point(10 + 4.9, 10 + 4.3) is True

    assert t.contains_point(10 + 4, 10 - 3) is False

    assert t.contains_point(10, 10 + t.height) is False


def test_triangle_contains_point_down():
    t = Triangle(cx=10, cy=10, size=10, direction="down")

    assert t.contains_point(10, 10) is True

    assert t.contains_point(10, 10 + 4.2) is True

    assert t.contains_point(10 + 4, 10 - 3) is True

    assert t.contains_point(10 + 4, 10 + 3) is False


def test_compute_average_color_random(color_triangle, red_image):
    color_triangle._compute_average_color_random(red_image)

    assert color_triangle.color == (255, 0, 0)


def test_compute_average_color_deterministic(color_triangle, red_image):
    color_triangle._compute_average_color_deterministic(red_image)

    assert color_triangle.color == (255, 0, 0)
