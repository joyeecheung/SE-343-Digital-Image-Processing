#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image


def filter2d(input_img, filter):
    """Apply 2-d filter to a 2-d image."""
    M, N = input_img.shape  # M is height, N is width
    n, m = len(filter), len(filter[0])  # m is height, n is width
    a, b = m / 2, n / 2
    # get transpose of the 1-d filter
    if (isinstance(filter, np.ndarray)):
        wt = filter.flatten()
    else:
        wt = np.array(filter).flatten()

    def correlation(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = np.full(n * m, input_img[x][y])  # pad with border duplicates
        # fill in available neighborhood
        for i in range(x - a, x + a + 1):
            for j in range(y - b, y + b + 1):
                if i > 0 and i < M and j > 0 and j < N:
                    z[(i - x + a) * n + j - y + b] = input_img[i, j]
        return np.dot(wt, z)

    result = [correlation(x, y) for x in range(M) for y in range(N)]
    return np.array(result).reshape(M, N)


def arithmetic_mean(img, size, raw=False):
    """Smooth the given image with arithmetic mean filter of given size."""
    m, n = size
    filter = np.full((m, n), float(1) / (m * n))  # averaging filter
    data = img if raw else np.array(img.getdata()).reshape(img.size[::-1])

    if raw:
        return filter2d(data, filter)
    else:
        return Image.fromarray(filter2d(data, filter)).convert(img.mode)


def img_to_float(img):
    return np.array(img.getdata(), dtype=np.float64).reshape(img.size[::-1])


def harmonic_mean(img, size):
    """Smooth the given image with harmonic mean filter of given size."""
    data = img_to_float(img)
    inverse = np.reciprocal(data)
    result = np.reciprocal(arithmetic_mean(inverse, size, True))
    return Image.fromarray(result).convert(img.mode)


def c_harmonic_mean(img, size, Q):
    data = img_to_float(img)
    numerator = np.power(data, Q + 1)
    denominator = np.power(data, Q)
    filter = np.full(size, 1.0)
    result = filter2d(numerator, filter) / filter2d(denominator, filter)
    return Image.fromarray(result).convert(img.mode)


def stat_filter2d(input_img, size, perc):
    """Apply a statistical filter to a 2-d image.

    max: perc=100
    min: perc=0
    median: perc=50
    """
    M, N = input_img.shape  # M is height, N is width
    m, n = size  # m is height, n is width
    a, b = m / 2, n / 2

    def correlation(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = []
        # fill in available neighborhood
        for i in range(x - a, x + a + 1):
            for j in range(y - b, y + b + 1):
                if i > 0 and i < M and j > 0 and j < N:
                    z.append(input_img[i, j])
        return np.percentile(z, perc)

    result = [correlation(x, y) for x in range(M) for y in range(N)]
    return np.array(result).reshape(M, N)


def median_filter(img, size):
    data = np.array(img.getdata()).reshape(img.size[::-1])
    result = stat_filter2d(data, size, 50)
    return Image.fromarray(result).convert(img.mode)


def max_filter(img, size):
    data = np.array(img.getdata()).reshape(img.size[::-1])
    result = stat_filter2d(data, size, 100)
    return Image.fromarray(result).convert(img.mode)


def min_filter(img, size):
    data = np.array(img.getdata()).reshape(img.size[::-1])
    result = stat_filter2d(data, size, 0)
    return Image.fromarray(result).convert(img.mode)
