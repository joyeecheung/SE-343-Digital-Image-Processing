#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from itertools import product
from itertools import chain
from numpy import arange
from scipy import interpolate
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", type=str, default="02.png")
source = parser.parse_args().source
file_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir, _ = os.path.split(file_dir)
filename = os.path.join(parent_dir, 'img', source)
result_dir = os.path.join(parent_dir, 'result')

print 'Source path: ' + filename
if not os.path.exists(filename):
    raise Exception("Source file doesn't exists!")
print 'Result directory: ' + result_dir


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


def quantize(input_img, level):
    pass

#def __main__():
    #get srcpath from cli
    #get destpath from cli
    #get func from cli
    #get args from cli

    #src = load(srcpath)
    #filter = filters[func]
    #dest = filter(src, *args)
    #dest.save(destpath)


def test_scale():
    input_img = Image.open(filename)
    cases = []
    cases.append([(192, 128), (96, 64), (48, 32), (24, 16), (12, 8)])
    cases.append([(300, 200), ])
    cases.append([(450, 300), ])
    cases.append([(500, 200), ])

    for case in cases:
        for size in case:
            result = scale(input_img, size)
            result_name = 'scale-%d-%d.png' % size
            result_path = os.path.join(result_dir, result_name)
            result.save(result_path)
            print 'Saved ' + result_path

if __name__ == "__main__":
    test_scale()
