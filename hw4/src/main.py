#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import numpy as np
from PIL import Image

from util import arithmetic_mean, harmonic_mean, c_harmonic_mean
from noise import gauss_noise, sap_noise


def test_filter(filename, result_dir):
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    a_mean_cases = [(3, 3), (9, 9)]
    for size in a_mean_cases:
        result = arithmetic_mean(im, size)
        savewith(result, 'arithmetic-mean-%d-%d.png' % size)

    h_mean_cases = [(3, 3), (9, 9)]
    for size in h_mean_cases:
        result = harmonic_mean(im, size)
        savewith(result, 'harmonic-mean-%d-%d.png' % size)

    c_h_mean_cases = [(3, 3), (9, 9)]
    for size in c_h_mean_cases:
        result = c_harmonic_mean(im, size, -1.5)
        savewith(result, 'c-harmonic-mean-%d-%d.png' % size)


def test_noise(filename, result_dir):
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    mean, var = 0, 40
    result = gauss_noise(im, mean, var)
    savewith(result, 'gauss-%d-%d.png' % (mean, var))

    ps, level = 0.2, 256
    result = sap_noise(im, level, ps=ps)
    savewith(result, 'salt-%d.png' % (int(100 * ps)))

    psap, level = 0.2, 256
    result = sap_noise(im, level, psap=psap)
    savewith(result, 'salt-and-pepper-%d.png' % (int(100 * psap)))


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

    # test_filter(os.path.join(source_path, 'task_1.png'), result_dir)
    test_noise(os.path.join(source_path, 'task_2.png'), result_dir)

if __name__ == "__main__":
    main()
