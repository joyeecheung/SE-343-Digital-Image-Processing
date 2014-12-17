#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image


class ImagePatches(object):
    """A list-like object of patches in an image.

    Usage:
        patches = ImagePatches(img, (patch_width, patch_height))
        first_patch = patches[0]
        last_patch = patches[patches.len - 1]
    """
    def __init__(self, im, patch_size):
        self.pixels = im
        self.H, self.W = self.pixels.shape
        self.w, self.h = patch_size
        self.len = (self.W - self.w + 1) * (self.H - self.h + 1)

    def __getitem__(self, key):
        x, y = key / (self.W - self.w + 1), key % (self.W - self.w + 1)
        return self.pixels[x:x+self.h, y:y+self.w]

    def __len__(self):
        return self.len


def view_as_window(img, patch_size):
    """
    Given an image and the desired patch size,
    return a list-like object of patches.
    """
    return ImagePatches(img, patch_size)


def create_image(mode, size, cb):
    """
    Create an image with given color `mode` and `size`,
    each pixel is generated by passing the row coordinate x
    and column coordinate y to the callback.
    """
    # create a new image
    out = Image.new(mode, size)
    width, height = size
    # draw the new image
    data = [cb(x, y) for y in range(height) for x in range(width)]
    out.putdata(data)
    return out


def filter2d(input_img, filter):
    """Apply 2-d filter to a 2-d image."""
    M, N = input_img.shape  # M is height, N is width
    n, m = len(filter), len(filter[0])  # m is height, n is width
    a, b = m / 2, n / 2
    patches = view_as_window(input_img, (n, m))
    pixels = patches.pixels
    # get transpose of the 1-d filter
    if (isinstance(filter, np.ndarray)):
        wt = filter.flatten()
    else:
        wt = np.array(filter).flatten()

    def correlation(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = np.full(n * m, pixels[y][x])  # pad with border duplicates
        # fill in available neighborhood
        for j in range(y - a, y + a + 1):
            for i in range(x - b, x + b + 1):
                if i > 0 and i < N and j > 0 and j < M:
                    z[(j - y + a) * n + i - x + b] = pixels[j][i]
        return np.dot(wt, z)

    result = [correlation(x, y) for y in range(M) for x in range(N)]
    return np.array(result).reshape(M, N)


def arithmetic_mean(img, size, raw=False):
    """Smooth the given image with arithmetic mean filter of given size."""
    m, n = size
    filter = np.full((m, n), float(1) / (m * n))  # averaging filter
    if raw:
        data = img
    else:
        data = np.array(img.getdata()).reshape(img.size[::-1])

    if raw:
        return filter2d(data, filter)
    else:
        return Image.fromarray(filter2d(data, filter)).convert(img.mode)


def harmonic_mean(img, size):
    """Smooth the given image with harmonic mean filter of given size."""
    inverse = np.array(img.getdata(), dtype=np.float64).reshape(img.size[::-1])
    inverse = np.reciprocal(inverse)
    result = np.reciprocal(arithmetic_mean(inverse, size, True))
    return Image.fromarray(result).convert(img.mode)
