#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bisect import bisect_right

from util import ImageForProcess, create_image


def NeighborFinder(values):
    """Factory for functions finding nearest neighbor in values.

    The parameter `values` should be a sorted list.
    Usage:
        find_neighbor = NeighborFinder(values)
        nearest_neighbbor_of_x = find_neighbor(x)
    """

    # insert means between consecutive values
    bounds = reduce(
        lambda x, y: x + [(x[-1] + y)/2, y] if x and y else [x, (x + y)/2, y],
        values)

    # binary search in the bounds to find the appropirate interval
    # notice that the inserted means must have odd indexes
    return lambda x: values[bisect_right(bounds, x)/2]


def quantize(input_img, level):
    """Quantize image for given grey level.

    The input must be a grey image.
    Usage:
        output_img = quantize(input_img, level)
    """
    # size of interval
    step = 256/(level - 1)
    # new color palette
    palette = [0] + list(range(step, 256 - step, step)) + [255]

    im = ImageForProcess(input_img)
    pixels = im.get_pixels()
    find_neighbor = NeighborFinder(palette)

    return create_image(
        input_img.mode,
        input_img.size,
        lambda x, y: find_neighbor(pixels[y][x]))
