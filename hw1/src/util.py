#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import arange
from scipy import interpolate


class ImageForProcess(object):
    def __init__(self, im):
        self._im = im
        self.width, self.height = self._im.size

    def __getattr__(self, key):
        if key == '_im':
            raise AttributeError()
        return getattr(self._im, key)

    def get_pixels(self, band=None):
        """Get the pixel data stored in a nested list.

        e.g.  [[1,2,3], [3,4,5] ...], each row is a horizontal line.
        """
        # by pixel
        data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.getpixel((x, y)))
            data.append(row)
        return data

        # use the whole data
        # data = list(self._im.getdata(band))
        # return [data[i:i+width] for i in range(0, len(data), width)]

    def get_interpolation(self, band=None):
        """Get the interpolation of specific band.

        band default to None i.e. a grey image
        """
        width, height = self.size
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
