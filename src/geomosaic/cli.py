import argparse
from pathlib import Path
from typing import get_args

import numpy as np
from PIL import Image

from geomosaic.hexagrid.hexagon import Orientation, generate_hexagonal_grid
from geomosaic.svg import export_to_svg


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
        "-s",
        "--size",
        type=float,
        default=15.0,
        help="Size of the hexagon (default is 15.0).",
    )

    parser.add_argument(
        "-m",
        "--margin",
        type=int,
        default=2,
        help="Number of additional rows and columns added to the grid dimensions (default: 2)",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose ouput."
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
        default="flat",
        help="Orientation of the hexagons: flat-top or pointy-top (default: 'flat')",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the png2svg CLI tool.
    """

    args = parse_arguments()

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
        print(f"Generating hexagonal grid ({args.orientation}-top)...")
    hex_grid = generate_hexagonal_grid(
        img.width,
        img.height,
        args.size,
        margin=args.margin,
        orientation=args.orientation,
    )
    for h in hex_grid:
        h.compute_color(
            np.asarray(img),
            method=args.color_sampling,
            step=args.step,
            sample_fraction=args.sample_fraction,
        )

    if verbose:
        print("Exporting to SVG format...")
    export_to_svg(hex_grid, img.width, img.height, output_path)

    print("Done.")


if __name__ == "__main__":
    main()
