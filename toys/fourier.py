#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from cmath import exp, pi, sqrt
import pylab as py
from scipy import fftpack, misc
from PIL import Image


def dftmtx(N):
    """Get discrete fourier transform matrix of size N x N."""
    n = np.asmatrix(np.arange(N))
    return np.exp((-1j * 2 * pi / N) * n.T * n)


def idftmtx(N):
    """Get inverse discrete fourier transform matrix of size N x N."""
    n = np.asmatrix(np.arange(N))
    return np.exp((1j * 2 * pi / N) * n.T * n)


def get_dft(data):
    """Get discrete fourier transform of data(numpy matrix/array)."""
    M, N = data.shape
    WM, WN = dftmtx(M), dftmtx(N)
    return WM * data * WN


def get_idft(data):
    """Get inverse discrete fourier transform of data(numpy matrix/array)."""
    M, N = data.shape
    WM, WN = idftmtx(M), idftmtx(N)
    return (1.0 / (M * N)) * WM * data * WN


def scale_intensity(f, typef, L=256):
    """Scale the intensities in the matrix to [0, L-1]."""
    fm = f - np.min(f)
    fs = (L - 1) * (fm / np.max(fm))
    return typef(fs)


def shift_dft(f):
    """Shift the fourier transform so that F(0,0) is in the center."""
    y = np.asarray(f)  # copy
    for k, n in enumerate(f.shape):
        mid = (n + 1)/2
        indices = np.concatenate((np.arange(mid, n), np.arange(mid)))
        y = np.take(y, indices, k)  # rearrange each axes
    return y


def get_power_spectrum(input_img):
    """Get the power spectrum image of a given image."""
    data = np.reshape(input_img.getdata(), input_img.size[::-1])
    fourier = shift_dft(get_dft(data))
    outdata = scale_intensity(np.log10(np.abs(fourier) ** 2), np.uint8)
    return Image.fromarray(outdata)


def show():
    """Show the power spectrum of lena."""
    input_img = Image.fromarray(misc.lena())
    psd = get_power_spectrum(input_img)
    psd.show()


def test():
    """Make sure my implementation is not too far from the scipy one."""
    scipyDFT = fftpack.fftshift(fftpack.fft2(misc.lena()))  # using fftpack
    myDFT = shift_dft(get_dft(misc.lena()))  # use my code
    errorF = np.abs(scipyDFT - myDFT) ** 2
    rangeF = (np.min(errorF), np.max(errorF))
    assert rangeF[1] < 1e-6
    print "[PASS] DFT, Error in (%.6e, %.6e)" % rangeF

    scipyIDFT = fftpack.ifft2(scipyDFT)
    myIDFT = get_idft(scipyDFT)
    errorIF = np.abs(scipyIDFT - myIDFT) ** 2
    rangeIF = (np.min(errorIF), np.max(errorIF))
    assert rangeIF[1] < 1e-6
    print "[PASS] IDFT, Error in (%.6e, %.6e)" % rangeIF

if __name__ == "__main__":
    test()
