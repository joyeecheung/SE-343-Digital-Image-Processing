#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import numpy as np
from PIL import Image

from util import arithmetic_mean, harmonic_mean, c_harmonic_mean


def test_filter(filename, result_dir):
    im = Image.open(filename)

    a_mean_cases = [(3, 3), (9, 9)]
    for size in a_mean_cases:
        result = arithmetic_mean(im, size)
        result_name = 'arithmetic-mean-%d-%d.png' % size
        result_path = os.path.join(result_dir, result_name)
        result.save(result_path)
        print '[Saved] ' + result_path

    h_mean_cases = [(3, 3), (9, 9)]
    for size in h_mean_cases:
        result = harmonic_mean(im, size)
        result_name = 'harmonic-mean-%d-%d.png' % size
        result_path = os.path.join(result_dir, result_name)
        result.save(result_path)
        print '[Saved] ' + result_path

    c_h_mean_cases = [(3, 3), (9, 9)]
    for size in c_h_mean_cases:
        result = c_harmonic_mean(im, size, -1.5)
        result_name = 'c-harmonic-mean-%d-%d.png' % size
        result_path = os.path.join(result_dir, result_name)
        result.save(result_path)
        print '[Saved] ' + result_path


def main():
    # ---------------- get the command line arguments --------------
    file_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir, _ = os.path.split(file_dir)
    source_path = os.path.join(parent_dir, 'img')
    result_dir = os.path.join(parent_dir, 'result')

    print 'Source path: ' + source_path
    if not os.path.exists(source_path):
        raise Exception("Source path doesn't exist!")
    print 'Result directory: ' + result_dir
    if not os.path.exists(result_dir):
        print "Result directory does not exist, created."
        os.makedirs(result_dir)

    test_filter(os.path.join(source_path, 'task_1.png'), result_dir)


if __name__ == "__main__":
    main()
