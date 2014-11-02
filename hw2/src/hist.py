#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import takewhile

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from util import create_image


def plot_hist(image):
    """Return a histogram figure of the histogram of the image."""
    fig, ax = plt.subplots()
    ax.set_xlim((0, 256))
    data = np.array(image.getdata())
    ax.hist(data, 256, color='black', edgecolor='none')
    return fig


def equalize(data, total, level=256):
    """
    Return a lookup table for equalizing the histogram of `data`
    with `total` number of pixels and the given intensity `level`.
    """
    pdf = map(lambda x: (x[1], float(x[0])/total), data)
    cdf = [sum(map(lambda x: x[1],
                   takewhile(lambda x: x[0] <= i,
                             pdf))) for i in range(level)]
    lookup = [round((level - 1) * i) for i in cdf]
    return lookup


def equalize_hist(input_img):
    """
    Apply histogram equalization to the given image
    and return the result.
    """
    colors = input_img.getcolors()
    pixel_count = input_img.size[0] * input_img.size[1]
    lookup = equalize(colors, pixel_count)
    return Image.eval(input_img, lambda x: lookup[x])
