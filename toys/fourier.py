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
    if len(data.shape) == 1:
        dim = len(data)
        return dftmtx(dim) * np.reshape(data, (dim, 1))
    return get_2d(data, lambda data: data * dftmtx(data.shape[1]))


def get_2d(data, fn):
    return fn(fn(data.T).T)


def get_idft(data):
    """Get inverse discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        dim = len(data)
        return (1.0 / dim) * idftmtx(dim) * np.reshape(data, (dim, 1))
    M, N = data.shape
    return (1.0 / (M * N)) * get_2d(data,
                                    lambda data: data * idftmtx(data.shape[1]))


def scale_intensity(f, typef, L=256):
    """Scale the intensities in the matrix to [0, L-1]."""
    fm = f - np.min(f)
    fs = (L - 1) * (fm / np.max(fm))
    return typef(fs)


def shift_dft(f):
    """Shift the fourier transform so that F(0,0) is in the center."""
    y = np.asarray(f)  # copy
    for k, n in enumerate(f.shape):
        mid = (n + 1) / 2
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
    lena = np.reshape(misc.lena(), (1024, 256))
    scipyShift = fftpack.fftshift(lena)
    myShift = shift_dft(lena)
    assert np.array_equal(scipyShift, myShift)
    print "[PASS] Shift"

    scipyDFT = fftpack.fftshift(fftpack.fft2(lena))  # using fftpack
    myDFT = shift_dft(get_dft(lena))  # use my code
    errorF = np.abs(scipyDFT - myDFT)
    rangeF = (np.min(errorF), np.max(errorF))
    assert np.allclose(scipyDFT, myDFT)
    print "[PASS] 2D-DFT, Error in (%.6e, %.6e)" % rangeF

    scipyIDFT = fftpack.ifft2(lena)
    myIDFT = get_idft(lena)
    errorIF = np.abs(scipyIDFT - myIDFT)
    rangeIF = (np.min(errorIF), np.max(errorIF))
    assert np.allclose(scipyIDFT, myIDFT)
    print "[PASS] 2D-IDFT, Error in (%.6e, %.6e)" % rangeIF

    data = np.random.rand(1, 1000)
    scipyDFT = fftpack.fft(data)  # using fftpack
    myDFT = get_dft(data)  # use my code
    errorF = np.abs(scipyDFT - myDFT)
    rangeF = (np.min(errorF), np.max(errorF))
    assert np.allclose(scipyDFT, myDFT)
    print "[PASS] 1D-DFT, Error in (%.6e, %.6e)" % rangeF

    scipyIDFT = fftpack.ifft(data)
    myIDFT = get_idft(data)
    errorIF = np.abs(scipyIDFT - myIDFT)
    rangeIF = (np.min(errorIF), np.max(errorIF))
    assert np.allclose(scipyIDFT, myIDFT)
    print "[PASS] 1D-IDFT, Error in (%.6e, %.6e)" % rangeIF


if __name__ == "__main__":
    test()
