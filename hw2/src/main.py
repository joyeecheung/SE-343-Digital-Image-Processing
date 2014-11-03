#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from PIL import Image
from random import randint

from util import create_image
from patch import view_as_window
from hist import plot_hist, equalize_hist
from filter import smooth, filter2d, laplacian, sobel


def test_plot(filename, result_dir):
    input_img = Image.open(filename)
    fig = plot_hist(input_img)
    result_path = os.path.join(result_dir, 'hist.png')
    fig.savefig(result_path)
    print '[Saved] ' + result_path


def test_equalize(filename, result_dir):
    input_img = Image.open(filename)
    output_img = equalize_hist(input_img)
    result_path = os.path.join(result_dir, 'equalize.png')
    output_img.save(result_path)
    print '[Saved] ' + result_path

    fig = plot_hist(output_img)
    plot_path = os.path.join(result_dir, 'hist-equalize.png')
    fig.savefig(plot_path)
    print '[Saved] ' + plot_path


def test_view_as_window(filename, result_dir):
    input_img = Image.open(filename)

    cases = [((96, 64),
              (20605, 36769, 52239, 4993, 16885, 16036, 6120, 2692)),
             ((50, 50),
              (21668, 11292, 44273, 51172, 53769, 67841, 5296, 53054))]
    for patch_size, keys in cases:
        windows = view_as_window(input_img, patch_size)
        for i, key in enumerate(keys):
            patch = windows[key]
            result = create_image(input_img.mode,
                                  patch_size,
                                  lambda x, y: patch[y][x])
            result_name = 'patch-%d-%d-%d.png' % (patch_size[0],
                                                  patch_size[1], i)
            result_path = os.path.join(result_dir, result_name)
            result.save(result_path)
            print '[Saved] ' + result_path


def test_smooth(filename, result_dir):
    input_img = Image.open(filename)

    cases = [(3, 3), (7, 7), (11, 11)]
    for case in cases:
        result = smooth(input_img, case)
        result_name = 'filter-smooth-%d-%d.png' % case
        result_path = os.path.join(result_dir, result_name)
        result.save(result_path)
        print '[Saved] ' + result_path


def test_laplacian(filename, result_dir):
    input_img = Image.open(filename)
    result = filter2d(input_img, laplacian)
    result_name = 'filter-laplacian.png'
    result_path = os.path.join(result_dir, result_name)
    result.save(result_path)
    print '[Saved] ' + result_path


def test_sobel(filename, result_dir):
    input_img = Image.open(filename)
    for index, case in enumerate(sobel):
        result = filter2d(input_img, case)
        result_name = 'filter-sobel-%d.png' % (index)
        result_path = os.path.join(result_dir, result_name)
        result.save(result_path)
        print '[Saved] ' + result_path


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
    if not os.path.exists(result_dir):
        raise Exception("Result directory doesn't exists!")

    test_plot(filename, result_dir)
    test_equalize(filename, result_dir)
    test_view_as_window(filename, result_dir)
    test_smooth(filename, result_dir)
    test_laplacian(filename, result_dir)
    test_sobel(filename, result_dir)

if __name__ == "__main__":
    main()
