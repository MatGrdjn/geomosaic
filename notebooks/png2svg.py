import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt

    from PIL import Image

    return Image, plt


@app.cell
def _(Image):
    image = Image.open("../input/screenshot.jpg")
    return (image,)


@app.cell
def _(image, plt):
    figure, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.imshow(image)
    ax.axis(False)

    plt.show()
    return


@app.cell
def _(image):
    channels= list(image.split())
    return


if __name__ == "__main__":
    app.run()
