from hexagrid.hexagon import Hexagon
from hexagrid.svg import export_to_svg


def test_export_to_svg(tmp_path):
    hex1 = Hexagon(cx=10, cy=10, size=5)
    hex1.color = (255, 0, 0)

    grid = [hex1]

    output_file = tmp_path / "test_output.svg"

    export_to_svg(grid, width=100, height=100, output_path=output_file)

    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")

    assert '<svg width="100" height="100"' in content
    assert 'xmlns="http://www.w3.org/2000/svg"' in content
    assert "<polygon" in content
    assert 'fill="rgb(255,0,0)"' in content
    assert "</svg>" in content
