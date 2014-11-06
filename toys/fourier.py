#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from cmath import exp, pi, sqrt
import pylab as py
from scipy import fftpack, misc
from PIL import Image


def dftmtx(N):
    n = np.asmatrix(np.arange(N))
    return np.exp((-1j * 2 * pi / N) * n.T * n)


def get_dft(data):
    M, N = data.shape
    WM, WN = dftmtx(M), dftmtx(N)
    return WM * data * WN


def scale_intensity(f, typef, L=256):
    fm = f - np.min(f)
    fs = (L - 1) * (fm / np.max(fm))
    return typef(fs)


def shift_dft(f):
    y = np.asarray(f)  # copy
    for k, n in enumerate(f.shape):
        mid = (n + 1)/2
        indices = np.concatenate((np.arange(mid, n), np.arange(mid)))
        y = np.take(y, indices, k)  # rearrange each axes
    return y


def get_power_spectrum(input_img):
    data = np.reshape(input_img.getdata(), input_img.size[::-1])
    fourier = shift_dft(get_dft(data))
    outdata = scale_intensity(np.log10(np.abs(fourier) ** 2), np.uint8)
    return Image.fromarray(outdata)


def show():
    input_img = Image.fromarray(misc.lena())
    psd = get_power_spectrum(input_img)
    psd.show()


def test():
    F1 = fftpack.fftshift(fftpack.fft2(misc.lena()))  # using fftpack
    F2 = shift_dft(get_dft(misc.lena()))  # use my code
    assert np.max(np.abs(F1-F2) ** 2) < 1e-6

if __name__ == "__main__":
    test()
