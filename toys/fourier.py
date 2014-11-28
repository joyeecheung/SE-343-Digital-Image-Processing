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
    return np.exp((-2j * pi / N) * n.T * n)


def idftmtx(N):
    """Get inverse discrete fourier transform matrix of size N x N."""
    n = np.asmatrix(np.arange(N))
    return np.exp((2j * pi / N) * n.T * n)


def fft(x):
    N = len(x)
    if (N <= 32):
        return get_dft(x)
    else:
        even = fft(x[0::2])
        odd = fft(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([even + factor[:N / 2] * odd,
                              even + factor[N / 2:] * odd])


def get_2d(data, fn):
    """Apply `fn` to each row, then to each column."""
    M, N = data.shape
    result = np.array(data) + 0j
    for i in xrange(M):
        result[i, :] = fn(result[i, :])
    for j in xrange(N):
        result[:, j] = fn(result[:, j])
    return result


def get_fft2d(data):
    return get_2d(data, fft)


def get_dft(data):
    """Get discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        return (dftmtx(len(data)) * data[:, None]).A1
    M, N = data.shape
    return dftmtx(M) * data * dftmtx(N)


def get_idft(data):
    """Get inverse discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        return ((1.0 / len(data)) * idftmtx(len(data)) * data[:, None]).A1
    M, N = data.shape
    return 1.0 / (M * N) * idftmtx(M) * data * idftmtx(N)


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

    scipyDFT = fftpack.fft2(lena)  # using fftpack
    myDFT = get_fft2d(lena)  # use my code
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

    data = np.random.rand(1024)
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
