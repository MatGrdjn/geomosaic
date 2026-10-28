import re
import sys
from pathlib import Path

import pytest
from PIL import Image

from geomosaic.cli import main, parse_arguments


@pytest.fixture
def input_image(tmp_path):
    img_path = tmp_path / "input_test.jpg"
    img = Image.new("RGB", (60, 60), color="blue")
    img.save(img_path)
    return img_path


def test_parse_arguments(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "geomosaic",
            "image.png",
            "-s",
            "20",
            "-m",
            "3",
            "-v",
            "--color-sampling",
            "random",
            "--step",
            "4",
            "--sample-fraction",
            "0.3",
            "--orientation",
            "pointy",
        ],
    )

    args = parse_arguments()

    assert args.input == Path("image.png")
    assert args.output is None
    assert args.size == 20.0
    assert args.margin == 3
    assert args.verbose is True
    assert args.color_sampling == "random"
    assert args.step == 4
    assert args.sample_fraction == 0.3
    assert args.orientation == "pointy"


def test_parse_arguments_defaults(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["geomosaic", "image.png"])

    args = parse_arguments()

    assert args.shape == "hexagon"
    assert args.orientation is None


def test_parse_arguments_triangle(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["geomosaic", "image.png", "--shape", "triangle"])

    args = parse_arguments()

    assert args.shape == "triangle"


def test_parse_arguments_invalid_shape(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["geomosaic", "image.png", "--shape", "square"])

    with pytest.raises(SystemExit):
        parse_arguments()


def test_parse_arguments_orientation_with_triangle(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["geomosaic", "image.png", "--shape", "triangle", "--orientation", "flat"],
    )

    with pytest.raises(SystemExit):
        parse_arguments()


def test_main_execution(tmp_path, monkeypatch, input_image):
    output_path = tmp_path / "output_test.svg"

    monkeypatch.setattr(
        sys, "argv", ["geomosaic", str(input_image), "-o", str(output_path), "-s", "10"]
    )

    main()

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "</svg>" in content
    assert "<polygon" in content


@pytest.mark.parametrize("shape, vertices", [("hexagon", 6), ("triangle", 3)])
def test_main_execution_shape(tmp_path, monkeypatch, input_image, shape, vertices):
    output_path = tmp_path / "output_test.svg"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "geomosaic",
            str(input_image),
            "-o",
            str(output_path),
            "-s",
            "10",
            "--shape",
            shape,
        ],
    )

    main()

    content = output_path.read_text(encoding="utf-8")
    points = re.findall(r'points="([^"]+)"', content)

    assert points
    assert all(len(p.split()) == vertices for p in points)
