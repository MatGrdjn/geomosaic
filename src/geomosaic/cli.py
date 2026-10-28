import argparse
from pathlib import Path
from typing import get_args

import numpy as np
from PIL import Image

from geomosaic.grid import Grid
from geomosaic.hexagrid import HexagonalGrid, Orientation
from geomosaic.triagrid import TriangularGrid

SHAPES = ["hexagon", "triangle"]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert images into hexagonal SVG mosaics."
    )

    parser.add_argument(
        "input", type=Path, help="Path to the input image (.png, .jpg, .jpeg, etc.)."
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Path to the output SVG file (default: same as input but with .svg extension).",
    )

    parser.add_argument(
        "--shape",
        type=str,
        choices=SHAPES,
        default="hexagon",
        help="Shape of the mosaic tiles (default: 'hexagon').",
    )

    parser.add_argument(
        "-s",
        "--size",
        type=float,
        default=15.0,
        help="Side length of the shapes (default: 15.0).",
    )

    parser.add_argument(
        "-m",
        "--margin",
        type=int,
        default=2,
        help="Number of additional rows and columns added to the grid dimensions (default: 2)",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )

    parser.add_argument(
        "--color-sampling",
        type=str,
        choices=["deterministic", "random"],
        default="deterministic",
        help="Color sampling method.",
    )

    parser.add_argument(
        "--step",
        type=int,
        default=2,
        help="Grid step size for determinsitic color sampling.",
    )

    parser.add_argument(
        "--sample-fraction",
        type=float,
        default=0.2,
        help="Sample fraction for random color sampling.",
    )

    parser.add_argument(
        "--orientation",
        type=str,
        choices=get_args(Orientation),
        default=None,
        help="Orientation of the hexagons: flat-top or pointy-top, "
        "only with --shape hexagon (default: 'flat').",
    )

    args = parser.parse_args()
    if args.shape != "hexagon" and args.orientation is not None:
        parser.error("--orientation is only available with --shape hexagon.")

    return args


def build_grid(args: argparse.Namespace, width: int, height: int) -> Grid:
    """Build the grid matching the shape chosen on the command line.

    Args:
        args (argparse.Namespace): The parsed command line arguments.
        width (int): Width of the image.
        height (int): Height of the image.

    Returns:
        Grid: The grid covering the image.
    """
    if args.shape == "hexagon":
        return HexagonalGrid(
            width,
            height,
            args.size,
            margin=args.margin,
            orientation=args.orientation or "flat",
        )

    return TriangularGrid(width, height, args.size, margin=args.margin)


def main() -> None:
    """
    Main entry point for the geomosaic CLI tool.
    """

    args = parse_arguments()
    if args.orientation is None:
        args.orientation = "flat"

    verbose = args.verbose

    if not args.input.is_file():
        print(f"Error: Input file '{args.input}' does not exist.")
        raise SystemExit(1)

    if verbose:
        print(f"Input file: '{args.input}'.")

    output_path = args.output
    if output_path is None:
        output_path = args.input.with_suffix(".svg")  # input_file_name.svg

    if output_path.exists():
        while True:
            answer = (
                input(
                    f"'{output_path}' already exists do you want to replace it ? (Y/N): "
                )
                .strip()
                .upper()
            )

            if answer == "Y":
                break

            elif answer == "N":
                raise SystemExit(0)

            else:
                print("Please enter Y or N.")

    if verbose:
        print(f"Output file: '{output_path}'.")

    if verbose:
        print("Loading image...")
    img = Image.open(args.input).convert("RGB")

    if verbose:
        print(
            f"Generating {args.shape} grid"
            + (f" ({args.orientation}-top)..." if args.shape == "hexagon" else "...")
        )
    grid = build_grid(args, img.width, img.height)

    grid.compute_colors(
        np.asarray(img),
        method=args.color_sampling,
        step=args.step,
        sample_fraction=args.sample_fraction,
    )

    if verbose:
        print("Exporting to SVG format...")
    grid.to_svg(output_path)

    print("Done.")


if __name__ == "__main__":
    main()
