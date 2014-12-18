#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import numpy as np
from PIL import Image

from filter import arithmetic_mean, geometric_mean
from filter import harmonic_mean, contraharmonic_mean
from filter import median_filter, max_filter, min_filter
from noise import add_noise
from hist import equalize_rgb_seperate, equalize_rgb_together


def test_filter(filename, result_dir):
    """2.2 Image Filtering"""
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    # 1. filter with 3 x 3 and 9 x 9 arithmetic mean filters
    a_mean_cases = [(3, 3), (9, 9)]
    for size in a_mean_cases:
        result = arithmetic_mean(im, size)
        savewith(result, 'arithmetic-mean-%d-%d.png' % size)

    # 2. filter  with 3 x 3 and 9 x 9 harmonic mean filters
    h_mean_cases = [(3, 3), (9, 9)]
    for size in h_mean_cases:
        result = harmonic_mean(im, size)
        savewith(result, 'harmonic-mean-%d-%d.png' % size)

    # 2. filter  with 3 x 3 and 9 x 9 contraharmonic mean filters
    #    with Q = −1.5.
    c_h_mean_cases = [(3, 3), (9, 9)]
    for size in c_h_mean_cases:
        result = contraharmonic_mean(im, size, -1.5)
        savewith(result, 'contraharmonic-mean-%d-%d.png' % size)


def test_gauss(filename, result_dir):
    """2.3.3 Guassian noise and denoising"""
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    # generate guassian noise
    mean, var = 0, 40
    noisy = add_noise(im, 'gauss', mean=mean, var=var)
    savewith(noisy, 'gauss-%d-%d.png' % (mean, var))

    # arithmetic mean filtering
    result = arithmetic_mean(noisy, (3, 3))
    savewith(result, 'gauss-arithmetic.png')

    # geometric mean filtering
    result = geometric_mean(noisy, (3, 3))
    savewith(result, 'gauss-geometric.png')

    # harmonic mean filtering
    result = harmonic_mean(noisy, (3, 3))
    savewith(result, 'gauss-harmonic.png')

    # contraharmonic mean filtering
    result = contraharmonic_mean(noisy, (3, 3), -1.5)
    savewith(result, 'gauss-contraharmonic.png')

    # median filtering
    result = median_filter(noisy, (3, 3))
    savewith(result, 'gauss-median.png')


def test_salt(filename, result_dir):
    """2.3.4 Salt noise and denoising"""
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    # add salt noise with ps=0.2
    ps = 0.2
    noisy = add_noise(im, 'sap', ps=ps)
    savewith(noisy, 'salt-%d.png' % (int(100 * ps)))

    # contraharmonic filtering
    q_neg, q_pos = 1.5, -1.5
    # Q < 0
    result = contraharmonic_mean(noisy, (3, 3), q_neg)
    savewith(result, 'salt-contraharmonic-%s.png' % (str(q_neg)))
    # Q > 0
    result = contraharmonic_mean(noisy, (3, 3), q_pos)
    savewith(result, 'salt-contraharmonic-%s.png' % (str(q_pos)))


def test_sap(filename, result_dir):
    """2.3.5 Salt-and-pepper noise and denoising"""
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    # add salt-and-pepper noise with ps=pp=0.2
    ps, pp = 0.2, 0.2
    noisy = add_noise(im, 'sap', ps=ps, pp=pp)
    savewith(noisy, 'sap-%d-%d.png' % (int(100 * ps), int(100 * pp)))

    # arithmetic mean filtering
    result = arithmetic_mean(noisy, (3, 3))
    savewith(result, 'sap-arithmetic.png')

    # harmonic mean filtering
    result = harmonic_mean(noisy, (3, 3))
    savewith(result, 'sap-harmonic.png')

    # contraharmonic mean filtering
    result = contraharmonic_mean(noisy, (3, 3), 11.5)
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


def test_hist(filename, result_dir):
    """"2.4 Histogram Equalization on Color Images"""
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    # 2.4.1 Do Histogram equalization on each channel separately,
    #       then rebuild an RGB image
    result = equalize_rgb_seperate(im)
    savewith(result, 'hist-seperate.png')

    # 2.4.2 Calculate the histogram for each channel, form an
    #       average histogram, then rebuild an RGB image with it.
    result = equalize_rgb_together(im)
    savewith(result, 'hist-together.png')


def main():
    # ------------ Ensure the project directory structure ---------
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

    # source image paths
    task_1_srcpath = os.path.join(source_path, 'task_1.png')
    task_2_srcpath = os.path.join(source_path, 'task_2.png')
    hist_srcpath = os.path.join(source_path, '02.png')

    # result paths
    task_1_destpath = os.path.join(result_dir, 'task1')
    task_2_destpath = os.path.join(result_dir, 'task2')
    gauss_path = os.path.join(task_2_destpath, 'gauss')
    salt_path = os.path.join(task_2_destpath, 'salt')
    sap_path = os.path.join(task_2_destpath, 'sap')
    hist_path = os.path.join(result_dir, 'hist')

    # make sure result paths exist
    destpaths = [task_1_destpath, task_2_destpath,
                 gauss_path, salt_path, sap_path, hist_path]
    for path in destpaths:
        if not os.path.exists(path):
            print "Created", path
            os.makedirs(path)

    # ------------ Generate results ---------

    # Task 2.2 Image Filtering
    test_filter(task_1_srcpath, task_1_destpath)

    # Task 2.3 Image Denoising
    # 2.3.3
    test_gauss(task_2_srcpath, gauss_path)
    # 2.3.4
    test_salt(task_2_srcpath, salt_path)
    # 2.3.5
    test_sap(task_2_srcpath, sap_path)

    # # Task 2.4 Histogram Equalization on Color Images
    test_hist(hist_srcpath, hist_path)

if __name__ == "__main__":
    main()
