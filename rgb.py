#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import click


def create_rgb(red=127):
    """Visualize the RGB color space

    input:
    red: The constant value of the red channel
    """
    # Create the three channels, R, G and B with all allowed
    # values in an 8-bit image
    size = 256
    r = np.ones(shape=(size, size), dtype=np.uint8) * red
    values = np.linspace(0, 255, size, dtype=np.uint8)
    gb_mesh = np.meshgrid(values, values)
    img = np.stack([r, *gb_mesh], axis=2)

    return img


def show_rgb_map(image, red, ax=None):
    """Show the RGB color space map

    input:
    image: The image to show
    red: The constant value of the red channel
    ax: The axes to plot on. If None, use plt.
    """
    # Use plt if ax is None, otherwise use ax
    if ax is None:
        _, ax = plt.subplots()

    # Title
    ax.set_title(f"RGB color space with Red={red}")

    # Axis labels
    ax.set_xlabel("Green")
    ax.set_ylabel("Blue")

    ax.imshow(image)

    return ax


@click.group()
def cli():
    pass


@cli.command()
@click.option("--red", default=127, help="The constant value of the red channel")
@click.option("--save-to", default=None, help="The file to save the image to")
def single(red, save_to):
    """Create a RGB color space image

    input:
    red: The constant value of the red channel
    save_to: The file to save the image to
    """
    img = create_rgb(red)

    # Show the image
    show_rgb_map(img, red)

    # Save image file if requested
    if save_to:
        plt.savefig(save_to)

    plt.show()


@cli.command()
@click.option(
    "--steps", default=3, help="The number of visualizations in the red channel range"
)
@click.option("--save-to", default=None, help="The file to save the image to")
def multiple(steps, save_to):
    """Create multiple RGB color space images

    input:
    steps: The number of visualizations in the red channel range
    save_to: The file to save the image to
    """
    # Create the images
    red = list(map(int, np.linspace(0, 255, steps)))
    images = [create_rgb(r) for r in red]

    # Plot the images in the same figure
    _, axes = plt.subplots(1, steps, figsize=(5 * steps, 5))
    for ax, img, r in zip(axes, images, red):
        show_rgb_map(img, r, ax)

    # Save image file if requested
    if save_to:
        plt.savefig(save_to)

    plt.show()


if __name__ == "__main__":
    cli()
