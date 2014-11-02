#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image


def create_image(mode, size, cb):
    # create a new image
    out = Image.new(mode, size)
    width, height = size
    # draw the new image
    data = [cb(x, y) for y in range(height) for x in range(width)]
    out.putdata(data)
    return out
