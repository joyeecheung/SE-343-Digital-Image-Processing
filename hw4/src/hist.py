#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import takewhile
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def plot_hist(image):
    """Return a histogram figure of the histogram of the image."""
    fig, ax = plt.subplots()
    ax.set_xlim((0, 256))
    data = np.array(image.getdata())
    ax.hist(data, 256, color='black', edgecolor='none')
    return fig


def equalize(data, total, level=256):
    """Return a lookup table for equalizing the histogram of `data`
       with `total` number of pixels and the given intensity `level`."""
    INTENSITY, COUNT, PDF = 0, 1, 1
    data = sorted(data, key=lambda x: x[INTENSITY])
    pdf = map(lambda x: (x[INTENSITY], float(x[COUNT])/total), data)
    cdf = [sum(map(lambda x: x[PDF],
                   takewhile(lambda x: x[INTENSITY] <= i,
                             pdf))) for i in range(level)]
    lookup = [round((level - 1) * i) for i in cdf]
    return lookup


def equalize_hist(input_img):
    """ Apply histogram equalization to the given image
        and return the result."""
    colors = Counter(input_img.getdata()).items()
    pixel_count = input_img.size[0] * input_img.size[1]
    lookup = equalize(colors, pixel_count)
    return Image.eval(input_img, lambda x: lookup[x])


def equalize_rgb_seperate(input_img):
    """Do Histogram equalization on each channel separately,
       then rebuild an RGB image with the tree processed channel."""
    equalized = map(equalize_hist, input_img.split())
    return Image.merge('RGB', equalized)


def equalize_rgb_together(input_img):
    """Calculate the histogram for each channel, form an
       average histogram, then rebuild an RGB image with it."""
    channels = input_img.split()
    data = map(lambda ch: list(ch.getdata()), channels)
    average_hist = [(k, v / 3) for k, v in Counter(sum(data, [])).items()]
    pixel_count = input_img.size[0] * input_img.size[1]
    lookup = equalize(average_hist, pixel_count)
    equalized = map(lambda ch: Image.eval(ch, lambda x: lookup[x]), channels)
    return Image.merge('RGB', equalized)
