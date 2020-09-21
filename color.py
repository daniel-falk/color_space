#!/usr/bin/env python3

from vi3o.image import imview, imsave
import cv2
import numpy as np


def show_cbcr(intensity):
    """Show the YCbCr color space

    Origin upper left corner, Cb on y-axis and Cr on x-axis.

    input:
    intensity: The constant value of the Y-channel (luminance)
    """
    # Create the three channels, Y, Cb and Cr with all allowed
    # values in an 8-bit image
    size = 256
    y = np.ones(shape=(size, size), dtype=np.uint8) * intensity
    cbcr_mesh = np.meshgrid(range(0, size), range(0, size))
    cbcr = map(lambda ch: ch.astype(np.uint8), cbcr_mesh)
    img = np.stack([y, *cbcr], axis=2)

    # Convert YCbCr color space to RGB since this is what the
    # image plot library expects
    rgb = cv2.cvtColor(img, cv2.COLOR_YCrCb2RGB)

    # Print values from upper left, lower right and center
    print("\nY=%d" % intensity)
    print(img[0, 0], img[-1, -1], img[size // 2, size // 2])
    print(rgb[0, 0], rgb[-1, -1], rgb[size // 2, size // 2])

    # Show image, wait form ENTER and save to disk
    imview(rgb)
    imsave(rgb, "rgb_%d.png" % intensity)


if __name__ == "__main__":
    for y in [0, 127, 255]:
        show_cbcr(y)
