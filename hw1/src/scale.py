#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import ImageForProcess, create_image
from numpy import arange


def scale(input_img, size):
    in_size = input_img.size
    in_width, in_height = in_size
    out_width, out_height = size

    # horizontal coordinates(relative)
    x = arange(0.0, in_width, float(in_width)/out_width)
    # vertical coordinates(relative)
    y = arange(0.0, in_height, float(in_height)/out_height)

    # get interpolated value
    im = ImageForProcess(input_img)
    ip = im.get_interpolation()
    data = ip(x, y)

    return create_image(input_img.mode, size, lambda x, y: data[y][x])
