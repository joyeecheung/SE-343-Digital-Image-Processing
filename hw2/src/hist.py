#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from itertools import takewhile
from util import create_image


def plot_hist(im):
    fig, ax = plt.subplots()
    ax.set_xlim((0, 256))
    data = np.array(im.getdata())
    ax.hist(data, 256, color='black', edgecolor='none', alpha=0.7)
    return fig


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
