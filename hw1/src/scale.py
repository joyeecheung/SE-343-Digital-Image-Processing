#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import arange

from util import ImageForProcess, create_image


def scale(input_img, size):
    """Scale image to given size.

    The input must be a grey image.
    Usage:
        output_img = scale(input_img, size)
    """

    if size == input_img.size:
        return create_image(
            input_img.mode, size,
            lambda x, y: input_img.getpixel((x, y)))

    # calculate measures of input/output
    in_size = input_img.size
    in_width, in_height = in_size
    out_width, out_height = size

    # relative horizontal coordinates of output images
    x = arange(0.0, in_width, float(in_width)/out_width)
    # relative vertical coordinates of output images
    y = arange(0.0, in_height, float(in_height)/out_height)

    # get interpolated value
    im = ImageForProcess(input_img)
    ip = im.get_interpolation()
    pixels = ip(y, x)

    return create_image(input_img.mode, size, lambda x, y: pixels[y][x])
