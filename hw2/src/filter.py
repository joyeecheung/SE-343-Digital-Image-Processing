#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from util import create_image
from patch import view_as_window


def filter2d(input_img, filter):
    N, M = input_img.size  # M is height, N is width
    m, n = len(filter), len(filter[0])  # m is height, n is width
    a, b = m / 2, n / 2
    patches = view_as_window(input_img, (n, m))
    pixels = patches.pixels
    if (isinstance(filter, np.ndarray)):
        wt = filter.flatten()
    else:
        wt = np.array(filter).flatten()

    def cb(x, y):
        z = np.zeros(n * m)
        for j in range(y - a, y + a + 1):
            for i in range(x - b, x + b + 1):
                if i > 0 and i < N and j > 0 and j < M:
                    z[(j - y + a) * n + i - x + b] = pixels[j][i]
        return np.dot(wt, z)

    return create_image(input_img.mode, input_img.size, cb)


def smooth(input_img, size):
    n, m = size
    filter = np.full((m, n), float(1) / (m * n))
    return filter2d(input_img, filter)


laplacian = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
sobel = [np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
         np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])]
