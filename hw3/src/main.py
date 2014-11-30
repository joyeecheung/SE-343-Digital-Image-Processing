#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from PIL import Image
from random import randint

from fourier import *
from filter import *


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

    input_img = Image.open(filename)
    data = np.reshape(input_img.getdata(), input_img.size[::-1])
    M, N = data.shape

    dft_shifted = shift_dft(dft2d(data, 1))
    dft_spec = scale_intensity(np.log(1 + np.abs(dft_shifted)))
    dft_spec_path = os.path.join(result_dir, 'dft-spectrum.png')
    Image.fromarray(dft_spec).convert('L').save(dft_spec_path)
    print '[Saved] ' + dft_spec_path

    dft_double = dft2d(dft2d(data, 1), -1).real
    dft_double_path = os.path.join(result_dir, 'dft-double.png')
    Image.fromarray(dft_double).convert('L').save(dft_double_path)
    print '[Saved] ' + dft_double_path

    fft_shifted = shift_dft(fft2d(pad(data), 1))
    fft_spec = scale_intensity(np.log(1 + np.abs(fft_shifted)))
    fft_spec_path = os.path.join(result_dir, 'fft-spectrum.png')
    Image.fromarray(fft_spec).convert('L').save(fft_spec_path)
    print '[Saved] ' + fft_spec_path

    fft_double = fft2d(fft2d(pad(data), 1), -1).real[:M, :N]
    fft_double_path = os.path.join(result_dir, 'fft-double.png')
    Image.fromarray(fft_double).convert('L').save(fft_double_path)
    print '[Saved] ' + fft_double_path

    filt_avg = filter2d_freq(input_img, average)
    filt_avg_path = os.path.join(result_dir, 'average-11-11.png')
    filt_avg.save(filt_avg_path)
    print '[Saved] ' + filt_avg_path

    filt_lap = filter2d_freq(input_img, laplacian)
    filt_lap_path = os.path.join(result_dir, 'laplacian-11-11.png')
    filt_lap.save(filt_lap_path)
    print '[Saved] ' + filt_lap_path


if __name__ == "__main__":
    main()
