import sys
from pathlib import Path

from PIL import Image

from hexagrid.cli import main, parse_arguments


def test_parse_arguments(monkeypatch):
    monkeypatch.setattr(
        sys, "argv", ["png2svg", "image.png", "-s", "20", "-m", "3", "-v"]
    )

    args = parse_arguments()

    assert args.input == Path("image.png")
    assert args.output is None
    assert args.size == 20.0
    assert args.margin == 3
    assert args.verbose is True


def test_main_execution(tmp_path, monkeypatch):
    img_path = tmp_path / "input_test.jpg"
    img = Image.new("RGB", (60, 60), color="blue")
    img.save(img_path)

    output_path = tmp_path / "output_test.svg"

    monkeypatch.setattr(
        sys, "argv", ["png2svg", str(img_path), "-o", str(output_path), "-s", "10"]
    )

    main()

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "</svg>" in content
    assert "<polygon" in content
