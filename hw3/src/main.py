#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from PIL import Image
from random import randint

from fourier import *
from filter import *


def main():
    # ---------------- get the command line arguments --------------
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
    if not os.path.exists(result_dir):
        raise Exception("Result directory doesn't exists!")

    def save_result(result, name, raw=True):
        path = os.path.join(result_dir, name)
        if raw:
            Image.fromarray(result).convert('L').save(path)
        else:
            result.save(path)
        print '[Saved] ' + path

    # ------------------- generate results ----------------------
    input_img = Image.open(filename)
    data = np.reshape(input_img.getdata(), input_img.size[::-1])
    M, N = data.shape

    # --------------------- DFT and IDFT ----------------
    dft_shifted = shift_dft(dft2d(data, 1))
    dft_spec = scale_intensity(np.log(1 + np.abs(dft_shifted)))
    save_result(dft_spec, 'dft-spectrum.png')

    dft_double = dft2d(dft2d(data, 1), -1).real
    save_result(dft_double, 'dft-double.png')

    # --------------------- FFT and IFFT ----------------
    fft_shifted = shift_dft(fft2d(pad_to_pow2(data), 1))
    fft_spec = scale_intensity(np.log(1 + np.abs(fft_shifted)))
    save_result(fft_spec, 'fft-spectrum.png')

    fft_double = fft2d(fft2d(pad_to_pow2(data), 1), -1).real[:M, :N]
    save_result(fft_double, 'fft-double.png')

    # --------------------- Frequency filters ----------------
    filt_avg = filter2d_freq(input_img, average)
    save_result(filt_avg, 'average-11-11.png', False)

    filt_lap = filter2d_freq(input_img, laplacian)
    save_result(filt_lap, 'laplacian.png', False)


if __name__ == "__main__":
    main()
