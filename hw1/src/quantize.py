#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import ImageForProcess, create_image
from math import log
from bisect import bisect_right


def find_neighbor(values):
    bounds = reduce(
        lambda x, y: x + [(x[-1] + y)/2, y] if x and y else [x, (x + y)/2, y],
        values)
    return lambda x: values[bisect_right(bounds, x)/2]


def quantize(input_img, level):
    step = 256/(level - 1)
    values = [0] + list(range(step, 256 - step, step)) + [255]
    im = ImageForProcess(input_img)
    data = im.get_pixels()
    f = find_neighbor(values)

    return create_image(
        input_img.mode,
        input_img.size,
        lambda x, y: f(data[y][x]))
