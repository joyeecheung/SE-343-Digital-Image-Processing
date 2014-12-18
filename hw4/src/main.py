#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import numpy as np
from PIL import Image

from filter import arithmetic_mean, harmonic_mean, contraharmonic_mean
from filter import geometric_mean
from filter import median_filter, max_filter, min_filter
from noise import gauss_noise, sap_noise
from hist import equalize_rgb_seperate, equalize_rgb_together


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
        result = contraharmonic_mean(im, size, -1.5)
        savewith(result, 'contraharmonic-mean-%d-%d.png' % size)


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
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    ps, level = 0.2, 256
    noisy = sap_noise(im, level, ps=ps)
    savewith(noisy, 'salt-%d.png' % (int(100 * ps)))

    q_neg, q_pos = 1.5, -1.5
    result = contraharmonic_mean(noisy, (3, 3), q_neg)
    savewith(result, 'salt-contraharmonic-%s.png' % (str(q_neg)))
    result = contraharmonic_mean(noisy, (3, 3), q_pos)
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
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print '[Saved] ' + result_path

    result = equalize_rgb_seperate(im)
    savewith(result, 'hist-seperate.png')

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

    task_1_srcpath = os.path.join(source_path, 'task_1.png')
    task_2_srcpath = os.path.join(source_path, 'task_2.png')
    hist_srcpath = os.path.join(source_path, '02.png')

    task_1_destpath = os.path.join(result_dir, 'task1')
    task_2_destpath = os.path.join(result_dir, 'task2')
    gauss_path = os.path.join(task_2_destpath, 'gauss')
    salt_path = os.path.join(task_2_destpath, 'salt')
    sap_path = os.path.join(task_2_destpath, 'sap')
    hist_path = os.path.join(result_dir, 'hist')

    destpaths = [task_1_destpath, task_2_destpath,
                 gauss_path, salt_path, sap_path, hist_path]
    for path in destpaths:
        if not os.path.exists(path):
            print "Created", path
            os.makedirs(path)

    # ------------ Generate results ---------

    # test_filter(task_1_srcpath, task_1_destpath)
    # test_gauss(task_2_srcpath, gauss_path)
    # test_salt(task_2_srcpath, salt_path)
    # test_sap(task_2_srcpath, sap_path)
    test_hist(hist_srcpath, hist_path)

if __name__ == "__main__":
    main()
