#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import click


def create_cbcr(luminance):
    """Visualize the YCbCr color space

    Origin upper left corner, Cb on y-axis and Cr on x-axis.

    input:
    luminance: The constant value of the Y-channel (luminance)
    """
    # Create the three channels, Y, Cb and Cr with all allowed
    # values in an 8-bit image
    size = 256
    y = np.ones(shape=(size, size), dtype=np.uint8) * luminance
    values = np.linspace(0, 255, size, dtype=np.uint8)
    cbcr_mesh = np.meshgrid(values, values)
    img = np.stack([y, *cbcr_mesh], axis=2)

    # Convert YCbCr color space to RGB since this is what the
    # image plot library expects
    rgb = cv2.cvtColor(img, cv2.COLOR_YCrCb2RGB)

    return rgb


def show_cbcr_map(image, luminance, ax=None):
    """Show the YCbCr color space map

    input:
    image: The image to show
    ax: The axes to plot on. If None, use plt.
    """

    # Use plt if ax is None, otherwise use ax
    if ax is None:
        _, ax = plt.subplots()

    # Title
    ax.set_title(f"YCbCr color space with Y={luminance}")

    # Axis labels
    ax.set_xlabel("Cr")
    ax.set_ylabel("Cb")

    ax.imshow(image)

    return ax


@click.group()
def cli():
    pass


@cli.command()
@click.option("--luminance", default=127, help="The luminance of the Y-channel")
@click.option("--save-to", default=None, help="The file to save the image to")
def single(luminance, save_to):
    """Create a YCbCr color space image

    input:
    luminance: The constant value of the Y-channel (luminance)
    """
    img = create_cbcr(luminance)

    # Show the image
    show_cbcr_map(img, luminance)

    # Save image file if requested
    if save_to:
        plt.savefig(save_to)

    plt.show()


@cli.command()
@click.option(
    "--steps", default=3, help="The number of visualizations in the luminance range"
)
@click.option("--save-to", default=None, help="The file to save the image to")
def multiple(steps, save_to):
    """Create multiple YCbCr color space images

    input:
    steps: The number of visualizations in the luminance range
    """
    # Create the images
    luminance = list(map(int, np.linspace(0, 255, steps)))
    images = [create_cbcr(luminance) for luminance in luminance]

    # Plot the images in the same figure
    _, axes = plt.subplots(1, steps, figsize=(5 * steps, 5))
    for ax, img, lum in zip(axes, images, luminance):
        show_cbcr_map(img, lum, ax)

    # Save image file if requested
    if save_to:
        plt.savefig(save_to)

    plt.show()


if __name__ == "__main__":
    cli()
