#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import numpy as np
from PIL import Image

from util import arithmetic_mean, harmonic_mean, c_harmonic_mean
from util import median_filter, max_filter, min_filter
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


def test_gauss(filename, result_dir):
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    # generate noise
    mean, var = 0, 40
    noisy = gauss_noise(im, mean, var)
    savewith(noisy, 'gauss-%d-%d.png' % (mean, var))

    # arithmetic mean filtering
    result = arithmetic_mean(noisy, (3, 3))
    savewith(result, 'gauss-arithmetic.png')

    # TODO: geometric mean filtering

    # harmonic mean filtering
    result = harmonic_mean(noisy, (3, 3))
    savewith(result, 'gauss-harmonic.png')

    # contraharmonic mean filtering
    result = c_harmonic_mean(noisy, (3, 3), -1.5)
    savewith(result, 'gauss-contraharmonic.png')

    # median filtering
    result = median_filter(noisy, (3, 3))
    savewith(result, 'gauss-median.png')


def test_salt(filename, result_dir):
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    ps, level = 0.2, 256
    noisy = sap_noise(im, level, ps=ps)
    savewith(noisy, 'salt-%d.png' % (int(100 * ps)))

    q_neg, q_pos = 1.5, -1.5
    result = c_harmonic_mean(noisy, (3, 3), q_neg)
    savewith(result, 'salt-contraharmonic-%s.png' % (str(q_neg)))
    result = c_harmonic_mean(noisy, (3, 3), q_pos)
    savewith(result, 'salt-contraharmonic-%s.png' % (str(q_pos)))


def test_sap(filename, result_dir):
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    psap, level = 0.2, 256
    noisy = sap_noise(im, level, psap=psap)
    savewith(noisy, 'sap-%d.png' % (int(100 * psap)))

    # arithmetic mean filtering
    result = arithmetic_mean(noisy, (3, 3))
    savewith(result, 'sap-arithmetic.png')

    # harmonic mean filtering
    result = harmonic_mean(noisy, (3, 3))
    savewith(result, 'sap-harmonic.png')

    # contraharmonic mean filtering
    result = c_harmonic_mean(noisy, (3, 3), -1.5)
    savewith(result, 'sap-contraharmonic.png')

    # max filtering
    result = max_filter(noisy, (3, 3))
    savewith(result, 'sap-max.png')

    # min filtering
    result = min_filter(noisy, (3, 3))
    savewith(result, 'sap-min.png')

    # median filtering
    result = median_filter(noisy, (3, 3))
    savewith(result, 'sap-median.png')


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

    task_1_path = os.path.join(source_path, 'task_1.png')
    task_2_path = os.path.join(source_path, 'task_2.png')

    #test_filter(task_1_path, result_dir)
    #test_gauss(task_2_path, result_dir)
    #test_salt(task_2_path, result_dir)
    test_sap(task_2_path, result_dir)

if __name__ == "__main__":
    main()
