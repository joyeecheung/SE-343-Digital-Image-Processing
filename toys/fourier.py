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
    """Vectorize & iterative FFT."""
    x = np.asarray(x, dtype=complex)
    N = len(x)
    temp = x.reshape((1, N))

    while temp.shape[0] < N:
        m, n = temp.shape
        odd, even = temp[:, n / 2:], temp[:, :n / 2]
        coff = np.exp(-1j * np.pi * np.arange(m) / m)[:, None]
        temp = np.vstack((even + coff * odd, even - coff * odd))

    return temp.ravel()


def get_2d(data, fn):
    """Apply `fn` to each row, then to each column."""
    result = np.copy(data)
    result = np.array([fn(row) for row in result])
    result = np.array([fn(col) for col in result.T])
    return result.T


def get_fft2d(data):
    return get_2d(data, fft)


def get_dft(data):
    """Get discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        return (dftmtx(len(data)) * data[:, None]).A1
    M, N = data.shape
    return np.asarray(dftmtx(M) * data * dftmtx(N))


def get_idft(data):
    """Get inverse discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        return ((1.0 / len(data)) * idftmtx(len(data)) * data[:, None]).A1
    M, N = data.shape
    return np.asarray(1.0 / (M * N) * idftmtx(M) * data * idftmtx(N))


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
    if np.array_equal(scipyShift, myShift):
        print "[PASS] Shift"
    else:
        print "[FALI] Shift"

    scipyDFT = fftpack.fft2(lena)  # using fftpack
    myDFT = get_dft(lena)  # use my code
    errorF = np.abs(scipyDFT - myDFT)
    rangeF = (np.min(errorF), np.max(errorF))
    if np.allclose(scipyDFT, myDFT):
        print "[PASS] 2D-DFT, Error in (%.6e, %.6e)" % rangeF
    else:
        print "[FAIL] 2D-DFT"

    scipyIDFT = fftpack.ifft2(lena)
    myIDFT = get_idft(lena)
    errorIF = np.abs(scipyIDFT - myIDFT)
    rangeIF = (np.min(errorIF), np.max(errorIF))
    if np.allclose(scipyIDFT, myIDFT):
        print "[PASS] 2D-IDFT, Error in (%.6e, %.6e)" % rangeIF
    else:
        print "[FAIL] 2D-IDFT"

    data = np.random.rand(1024)
    scipyDFT = fftpack.fft(data)  # using fftpack
    myDFT = get_dft(data)  # use my code
    errorF = np.abs(scipyDFT - myDFT)
    rangeF = (np.min(errorF), np.max(errorF))
    if np.allclose(scipyDFT, myDFT):
        print "[PASS] 1D-DFT, Error in (%.6e, %.6e)" % rangeF
    else:
        print "[FAIL] 1D-DFT"

    scipyIDFT = fftpack.ifft(data)
    myIDFT = get_idft(data)
    errorIF = np.abs(scipyIDFT - myIDFT)
    rangeIF = (np.min(errorIF), np.max(errorIF))
    if np.allclose(scipyIDFT, myIDFT):
        print "[PASS] 1D-IDFT, Error in (%.6e, %.6e)" % rangeIF
    else:
        print "[FAIL] 1D-IDFT"

    scipyDFT = fftpack.fft2(lena)  # using fftpack
    myDFT = get_fft2d(lena)  # use my code
    errorF = np.abs(scipyDFT - myDFT)
    rangeF = (np.min(errorF), np.max(errorF))
    if np.allclose(scipyDFT, myDFT):
        print "[PASS] 2D-FFT, Error in (%.6e, %.6e)" % rangeF
    else:
        print "[FAIL] 2D-FFT"

    scipyDFT = fftpack.fft(data)  # using fftpack
    myDFT = fft(data)  # use my code
    errorF = np.abs(scipyDFT - myDFT)
    rangeF = (np.min(errorF), np.max(errorF))
    if np.allclose(scipyDFT, myDFT):
        print "[PASS] 1D-FFT, Error in (%.6e, %.6e)" % rangeF
    else:
        print "[FAIL] 1D-FFT"


if __name__ == "__main__":
    test()
    # myDFT = get_fft2d(lena)  # use my code
