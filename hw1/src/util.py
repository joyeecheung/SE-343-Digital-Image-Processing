#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import arange
from scipy import interpolate


class ImageForProcess():
    def __init__(self, im):
        self.im = im
        self.width, self.height = self.im.size

    def get_pixels(self, band=None):
        """Get the pixel data stored in a nested list.

        e.g.  [[1,2,3], [3,4,5] ...], each row is a horizontal line.
        """
        # by pixel
        data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.im.getpixel((x, y)))
            data.append(row)
        return data

        # use the whole data
        # data = list(im.getdata(band))
        # return [data[i:i+width] for i in range(0, len(data), width)]

    def get_interpolation(self, band=None):
        """Get the interpolation of specific band.

        band default to None i.e. a grey image
        """
        width, height = self.im.size
        x, y = arange(self.width), arange(height)
        z = self.get_pixels(band)
        return interpolate.interp2d(x, y, z)


def create_image(mode, size, cb):
    # create a new image
    out = Image.new(mode, size)

    # draw the new image
    for y in range(size[1]):
        for x in range(size[0]):
            out.putpixel((x, y), cb(x, y))

    return out
