# /// script
# dependencies = [
#     "geomosaic",
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy",
#     "pillow",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="full")


@app.cell
def _():
    import io
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    from hexagrid.hexagon import generate_hexagonal_grid, Hexagon
    from hexagrid.svg import export_to_svg
    from PIL import Image

    return Image, export_to_svg, generate_hexagonal_grid, io, mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hexagrid : Convert an image (.png, .jpg, etc.) into a SVG mosaic

    Drag and drop an image and adjust parameters to generate the vectorized mosaic.
    """)
    return


@app.cell
def _(mo):
    file_picker = mo.ui.file(
        filetypes=[".png", ".jpg", ".jpeg", ".webp"],
        label="Choose an image to convert"
    )

    size_input = mo.ui.number(
        start=1.0, stop=100.0, step=1.0, value=15.0,
        label="Size of the hexagons (flat-top)"
    )

    margin_input = mo.ui.number(
        start=0, stop=10, step=1, value=2,
        label="Grid margin"
    )

    mo.vstack([file_picker, size_input, margin_input])
    return file_picker, margin_input, size_input


@app.cell
def _(
    Image,
    export_to_svg,
    file_picker,
    generate_hexagonal_grid,
    io,
    margin_input,
    mo,
    np,
    size_input,
):
    if file_picker.value:
        uploaded_file = file_picker.value[0]

        img = Image.open(io.BytesIO(uploaded_file.contents)).convert("RGB")

        hex_grid = generate_hexagonal_grid(
                img.width, img.height, 
                size_input.value, 
                margin=int(margin_input.value)
        )

        for h in hex_grid:
            h.compute_average_color_random(np.asarray(img))

        output_filename = f"output_{uploaded_file.name.rsplit('.', 1)[0]}.svg"
        export_to_svg(hex_grid, img.width, img.height, output_filename)

        result = mo.hstack([
                mo.vstack([
                    mo.md("**Original Image**"),
                    mo.image(src=uploaded_file.contents, width=500)
                ]),
                mo.vstack([
                    mo.md("**SVG Mosaic**"),
                    mo.image(src=f"output_{uploaded_file.name.rsplit('.', 1)[0]}.svg", width=500)
                ]),
                mo.vstack([
                    mo.md("**Result**"),
                    mo.md(f"""
                    * **Generated file:** `{output_filename}`
                    * **Hexagons size:** {size_input.value}
                    * **Hexagon number:** {len(hex_grid)}
                    """)
                ])
        ])

    else:
        result = mo.md("### Please select an image to start the conversion.")

    result
    return


if __name__ == "__main__":
    app.run()
