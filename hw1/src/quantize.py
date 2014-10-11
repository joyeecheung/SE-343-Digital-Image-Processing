#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import ImageForProcess, create_image
from math import log
from bisect import bisect_left


def quantize(input_img, level):
    step = 256/(level - 1)
    bounds = [0] + list(range(step, 256 - step, step)) + [255]
    im = ImageForProcess(input_img)
    data = im.get_pixels()

    def find_neighbor(x):
        if x == 0:
            return 0
        else:
            idx = bisect_left(bounds, x)
            mean = (bounds[idx - 1] + bounds[idx]) / 2
            return bounds[idx - 1] if x < mean else bounds[idx]

    return create_image(
        input_img.mode,
        input_img.size,
        lambda x, y: find_neighbor(data[y][x]))
