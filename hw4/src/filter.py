#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from util import img_to_array, array_to_img


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

    def correlate(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = np.full(n * m, input_img[x, y])  # pad with border duplicates
        # fill in available neighborhood
        for i in xrange(x - a, x + a + 1):
            for j in xrange(y - b, y + b + 1):
                if i >= 0 and i < M and j >= 0 and j < N:
                    z[(i - x + a) * n + j - y + b] = input_img[i, j]
        return np.dot(wt, z)

    xx, yy = np.meshgrid(xrange(M), xrange(N), indexing='ij')
    vf = np.vectorize(correlate)
    return vf(xx, yy)


def arithmetic_mean(img, size, raw=False):
    """Smooth the given image with arithmetic mean filter of given size."""
    m, n = size
    filter = np.full((m, n), float(1) / (m * n))  # averaging filter
    data = img if raw else img_to_array(img)

    if raw:
        return filter2d(data, filter)
    else:
        return array_to_img(filter2d(data, filter), img.mode)


def harmonic_mean(img, size):
    """Smooth the given image with harmonic mean filter of given size."""
    data = img_to_array(img, dtype=np.float64)
    inverse = np.reciprocal(data)
    result = np.reciprocal(arithmetic_mean(inverse, size, True))
    return array_to_img(result, img.mode)


def contraharmonic_mean(img, size, Q):
    data = img_to_array(img, dtype=np.float64)
    numerator = np.power(data, Q + 1)
    denominator = np.power(data, Q)
    filter = np.full(size, 1.0)
    result = filter2d(numerator, filter) / filter2d(denominator, filter)
    return array_to_img(result, img.mode)


def stat_filter2d(input_img, size, perc):
    """Apply a statistical filter to a 2-d image.

    max: perc=100
    min: perc=0
    median: perc=50
    """
    M, N = input_img.shape  # M is height, N is width
    m, n = size  # m is height, n is width
    a, b = m / 2, n / 2

    def correlate(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = []
        # fill in available neighborhood
        for i in xrange(x - a, x + a + 1):
            for j in xrange(y - b, y + b + 1):
                if i >= 0 and i < M and j >= 0 and j < N:
                    z.append(input_img[i, j])
        return np.percentile(z, perc)

    xx, yy = np.meshgrid(xrange(M), xrange(N), indexing='ij')
    vf = np.vectorize(correlate)
    return vf(xx, yy)


def median_filter(img, size):
    data = img_to_array(img)
    result = stat_filter2d(data, size, 50)
    return array_to_img(result, img.mode)


def max_filter(img, size):
    data = img_to_array(img)
    result = stat_filter2d(data, size, 100)
    return array_to_img(result, img.mode)


def min_filter(img, size):
    data = img_to_array(img)
    result = stat_filter2d(data, size, 0)
    return array_to_img(result, img.mode)


def geometric_mean(input_img, size):
    """Apply geometric mean filter to a 2-d image."""
    data = img_to_array(input_img, dtype=np.float64)
    M, N = data.shape  # M is height, N is width
    m, n = size  # m is height, n is width
    a, b = m / 2, n / 2

    def correlate(x, y):
        z = np.full(n * m, data[x, y])  # pad with border duplicates
        # fill in available neighborhood
        for i in xrange(x - a, x + a + 1):
            for j in xrange(y - b, y + b + 1):
                if i >= 0 and i < M and j >= 0 and j < N:
                    z[(i - x + a) * n + j - y + b] = data[i, j]
        # calculate power first to avoid overflow
        return np.prod(np.power(z, 1.0 / (m * n)))

    xx, yy = np.meshgrid(xrange(M), xrange(N), indexing='ij')
    vf = np.vectorize(correlate)
    result = vf(xx, yy)
    return array_to_img(result, input_img.mode)
