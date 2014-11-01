#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from itertools import takewhile
from util import *

r = [(790, 0), (1023, 1), (850, 2), (656, 3),
     (329, 4), (245, 5), (122, 6), (81, 7)]


def plot_hist(im):
    fig, ax = plt.subplots()
    ax.set_xlim((0, 256))
    data = np.array(im.getdata())
    ax.hist(data, 256, color='black', edgecolor='none', alpha=0.7)
    return fig


def test_plot(filename, result_dir):
    input_img = Image.open(filename)
    fig = plot_hist(input_img)
    result_path = os.path.join(result_dir, 'hist.png')
    fig.savefig(result_path)


def equalize(data, total, level=256):
    pdf = map(lambda x: (x[1], float(x[0])/total), data)
    cdf = [sum(map(lambda x: x[1],
                   takewhile(lambda x: x[0] <= i,
                             pdf))) for i in range(level)]
    table = [round((level - 1) * i) for i in cdf]
    return table


def equalize_hist(input_img):
    colors = input_img.getcolors()
    pixel_count = input_img.size[0] * input_img.size[1]
    lookup = equalize(colors, pixel_count)
    return create_image(input_img.mode,
                        input_img.size,
                        lambda x, y: lookup[input_img.getpixel((x, y))])


def test_equalize(filename, result_dir):
    input_img = Image.open(filename)
    output_img = equalize_hist(input_img)
    result_path = os.path.join(result_dir, 'equalize.png')
    output_img.save(result_path)
    fig = plot_hist(output_img)
    plot_path = os.path.join(result_dir, 'hist-equalize.png')
    fig.savefig(plot_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, default="02.png")
    source = parser.parse_args().source

    # absolute path to the directory of this .py
    file_dir = os.path.dirname(os.path.realpath(__file__))
    # absolute path to the parent directory of this .py
    parent_dir, _ = os.path.split(file_dir)
    # absolute path to the image file to process
    filename = os.path.join(parent_dir, 'img', source)
    # absolute path to the result directory
    result_dir = os.path.join(parent_dir, 'result')

    print 'Source path: ' + filename
    if not os.path.exists(filename):
        raise Exception("Source file doesn't exists!")
    print 'Result directory: ' + result_dir

    test_plot(filename, result_dir)
    test_equalize(filename, result_dir)


if __name__ == "__main__":
    main()
